from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import psycopg2
import psycopg2.extras
import random
import logging
import os
import time

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s", "level":"%(levelname)s", "message":"%(message)s"}'
)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'postgres'),
    'database': os.getenv('DB_NAME', 'transactions'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

def get_db_connection():
    """Create database connection with retry logic"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            return conn
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database connection attempt {attempt + 1} failed, retrying...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Database connection failed after {max_retries} attempts")
                raise

@app.route("/health")
def health():
    """Deep health check with database connectivity"""
    health_status = {
        "status": "healthy",
        "service": "flask_api",
        "checks": {}
    }
    
    # Check database connection
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        health_status["checks"]["database"] = "ok"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = f"error: {str(e)}"
        logger.error(f"Health check failed: {e}")
        return jsonify(health_status), 503
    
    return jsonify(health_status), 200

@app.route("/transactions")
def get_transactions():
    """Get recent transactions from database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute("""
            SELECT id, amount, status, user_id, created_at 
            FROM transactions 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        
        transactions = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert to JSON-serializable format
        result = []
        for tx in transactions:
            result.append({
                'id': tx['id'],
                'amount': float(tx['amount']),
                'status': tx['status'],
                'user_id': tx['user_id'],
                'created_at': tx['created_at'].isoformat() if tx['created_at'] else None
            })
        
        logger.info(f"Retrieved {len(result)} transactions")
        return jsonify({"transactions": result, "count": len(result)}), 200
    
    except Exception as e:
        logger.error(f"Failed to retrieve transactions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/transactions/create", methods=['POST'])
def create_transaction():
    """Create a new transaction (simulates payment processing)"""
    try:
        # Simulate occasional errors (5% error rate)
        if random.random() < 0.05:
            raise Exception("Payment gateway timeout")
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Generate random transaction
        amount = round(random.uniform(10.0, 999.99), 2)
        user_id = f"user_{random.randint(1, 1000):03d}"
        status = random.choice(['completed', 'completed', 'completed', 'pending'])
        
        cur.execute(
            "INSERT INTO transactions (amount, status, user_id) VALUES (%s, %s, %s) RETURNING id",
            (amount, status, user_id)
        )
        
        tx_id = cur.fetchone()[0]
        conn.commit()
        
        cur.close()
        conn.close()
        
        logger.info(f"Transaction {tx_id} created: ${amount} - {status}")
        
        return jsonify({
            "transaction_id": tx_id,
            "amount": amount,
            "status": status,
            "user_id": user_id
        }), 201
    
    except Exception as e:
        logger.error(f"Transaction creation failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/error")
def error():
    """Intentional error endpoint for testing alerts"""
    raise Exception("Intentional error for testing")

if __name__ == "__main__":
    logger.info("Starting Flask API on port 8000")
    app.run(host="0.0.0.0", port=8000)