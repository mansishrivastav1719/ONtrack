from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            # Connect to MongoDB
            self.client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database and collection
            self.db = self.client[config.MONGO_DB]
            self.collection = self.db[config.MONGO_COLLECTION]
            
            logger.info(f"✅ Connected to MongoDB: {config.MONGO_URI}")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            self.client = None
            self.db = None
            self.collection = None
            return False
    
    def check_connection(self):
        """Check if database is connected"""
        if self.client is None:
            return False
        try:
            self.client.admin.command('ping')
            return True
        except:
            return False
    
    def insert_student(self, student_data):
        """Insert a single student record"""
        try:
            result = self.collection.insert_one(student_data)
            logger.info(f"✅ Inserted student with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"❌ Insert failed: {e}")
            return None
    
    def insert_many_students(self, students_list):
        """Insert multiple student records"""
        try:
            result = self.collection.insert_many(students_list)
            logger.info(f"✅ Inserted {len(result.inserted_ids)} students")
            return result.inserted_ids
        except Exception as e:
            logger.error(f"❌ Bulk insert failed: {e}")
            return None
    
    def get_all_students(self, limit=100):
        """Get all students with optional limit"""
        try:
            cursor = self.collection.find().limit(limit)
            students = list(cursor)
            logger.info(f"✅ Retrieved {len(students)} students")
            return students
        except Exception as e:
            logger.error(f"❌ Failed to retrieve students: {e}")
            return []
    
    def get_student_by_id(self, student_id):
        """Get a specific student by ID"""
        try:
            student = self.collection.find_one({"student_id": student_id})
            if student:
                logger.info(f"✅ Found student: {student_id}")
            else:
                logger.info(f"❌ Student not found: {student_id}")
            return student
        except Exception as e:
            logger.error(f"❌ Failed to retrieve student {student_id}: {e}")
            return None
    
    def update_student_prediction(self, student_id, prediction_data):
        """Update a student's prediction results"""
        try:
            result = self.collection.update_one(
                {"student_id": student_id},
                {"$set": {"prediction": prediction_data}}
            )
            if result.modified_count > 0:
                logger.info(f"✅ Updated prediction for student: {student_id}")
            else:
                logger.info(f"❌ No update for student: {student_id}")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Update failed for {student_id}: {e}")
            return False
    
    def get_risk_distribution(self):
        """Get count of students by risk level"""
        try:
            pipeline = [
                {"$group": {"_id": "$prediction.risk_level", "count": {"$sum": 1}}}
            ]
            results = self.collection.aggregate(pipeline)
            distribution = {item["_id"]: item["count"] for item in results}
            logger.info(f"✅ Risk distribution: {distribution}")
            return distribution
        except Exception as e:
            logger.error(f"❌ Failed to get risk distribution: {e}")
            return {"Low": 0, "Medium": 0, "High": 0}
    
    def delete_all_students(self):
        """Delete all students (use carefully!)"""
        try:
            result = self.collection.delete_many({})
            logger.warning(f"⚠️ Deleted {result.deleted_count} students")
            return result.deleted_count
        except Exception as e:
            logger.error(f"❌ Delete failed: {e}")
            return 0

# Create a global database instance
db = MongoDB()