import os
import random
import schedule
import time
from src.openai_service import openai_service
from src.linkedin_service import linkedin_service
from src.exceptions import ServiceException

def get_random_topic(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Topics file not found at {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        topics = [line.strip() for line in f if line.strip()]
    if not topics:
        raise ValueError("No topics found in topics.txt")
    return random.choice(topics)

def job():
    print(f"Starting scheduled task at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        topics_path = os.path.join("src", "topics.txt")
        topic = get_random_topic(topics_path)
        print(f"Selected topic: {topic}")
        
        post_content = openai_service.generate_linkedin_post(topic)
        print("Post content generated successfully.")
        
        user_id = linkedin_service.get_user_id()
        if not user_id:
            raise ServiceException("Failed to get user ID.")
        
        success = linkedin_service.post_to_linkedin(post_content, f"urn:li:person:{user_id}")
        if success:
            print("Post published on LinkedIn.")
        else:
            print("Failed to publish post.")
            
    except ServiceException as e:
        print(f"Service error in job execution: {e.message}")
    except Exception as e:
        print(f"Unexpected error in job execution: {e}")

def main():
    # Schedule: Every Wednesday at 08:00
    schedule.every().wednesday.at("08:00").do(job)
    
    print("Scheduler started. Waiting for Wednesday 08:00 AM...")
    
    # For testing purposes, you might want to run it once immediately
    # job() 

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()