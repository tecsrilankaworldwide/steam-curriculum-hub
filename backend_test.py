import requests
import sys
import json
from datetime import datetime

class GlobalSTEAMHubTester:
    def __init__(self, base_url="https://tech-curriculum-9.preview.emergentagent.com"):
        self.base_url = base_url
        self.student_token = None
        self.admin_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.student_user_id = None
        self.admin_user_id = None
        self.created_lesson_id = None
        self.test_inquiry_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = {'Content-Type': 'application/json'}
        if headers:
            request_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=request_headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=request_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=request_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=request_headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict) and len(response_data) <= 3:
                        print(f"   Response: {response_data}")
                except:
                    print(f"   Response: Non-JSON or large response")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"   Error: {response.text}")
                except:
                    print(f"   Error: Could not read response")

            return success, response.json() if success and response.text else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test health check endpoint"""
        success, response = self.run_test(
            "Health Check",
            "GET",
            "api/health",
            200
        )
        return success

    def test_student_registration(self):
        """Test student registration"""
        success, response = self.run_test(
            "Student Registration",
            "POST",
            "api/auth/register",
            200,
            data={
                "name": "Test Student",
                "email": "student@test.com", 
                "password": "student123",
                "role": "student"
            }
        )
        if success and 'access_token' in response:
            self.student_token = response['access_token']
            if 'user' in response:
                self.student_user_id = response['user'].get('id')
            print(f"   ✅ Student token obtained")
            return True
        return False

    def test_admin_registration(self):
        """Test admin registration"""
        success, response = self.run_test(
            "Admin Registration",
            "POST", 
            "api/auth/register",
            200,
            data={
                "name": "Test Admin",
                "email": "admin@steamhub.edu",
                "password": "admin123",
                "role": "admin"
            }
        )
        if success and 'access_token' in response:
            self.admin_token = response['access_token']
            if 'user' in response:
                self.admin_user_id = response['user'].get('id')
            print(f"   ✅ Admin token obtained")
            return True
        return False

    def test_student_login(self):
        """Test student login with provided credentials"""
        success, response = self.run_test(
            "Student Login",
            "POST",
            "api/auth/login",
            200,
            data={
                "email": "student@test.com",
                "password": "student123"
            }
        )
        if success and 'access_token' in response:
            self.student_token = response['access_token']
            if 'user' in response:
                self.student_user_id = response['user'].get('id')
            return True
        return False

    def test_admin_login(self):
        """Test admin login with provided credentials"""
        success, response = self.run_test(
            "Admin Login",
            "POST",
            "api/auth/login", 
            200,
            data={
                "email": "admin@steamhub.edu",
                "password": "admin123"
            }
        )
        if success and 'access_token' in response:
            self.admin_token = response['access_token']
            if 'user' in response:
                self.admin_user_id = response['user'].get('id')
            return True
        return False

    def test_get_lessons(self):
        """Test getting lessons with filters"""
        # Test basic lesson retrieval
        success, response = self.run_test(
            "Get All Lessons",
            "GET",
            "api/lessons",
            200
        )
        
        if success and 'lessons' in response:
            lessons = response['lessons']
            print(f"   📚 Found {len(lessons)} lessons")
            
            # Test AI-STEAM curriculum filter (should have 1000+ lessons)
            success2, response2 = self.run_test(
                "Filter by AI-STEAM Curriculum",
                "GET", 
                "api/lessons?curriculum=AI-STEAM",
                200
            )
            
            if success2 and 'lessons' in response2:
                ai_lessons = response2['lessons']
                print(f"   🤖 Found {len(ai_lessons)} AI-STEAM lessons")
                if len(ai_lessons) < 100:
                    print(f"   ⚠️ Expected 1000+ AI-STEAM lessons, only found {len(ai_lessons)}")
                
                # Check for Sinhala translations in AI lessons
                sinhala_count = 0
                for lesson in ai_lessons[:10]:  # Check first 10
                    if lesson.get('title', {}).get('si'):
                        sinhala_count += 1
                print(f"   🇱🇰 Found Sinhala translations in {sinhala_count}/10 checked lessons")
            
            # Test age group filter
            success3, response3 = self.run_test(
                "Filter by Age Group 5-7",
                "GET",
                "api/lessons?age_group=5-7", 
                200
            )
            
            # Test subject filter
            success4, response4 = self.run_test(
                "Filter by AI Subject",
                "GET",
                "api/lessons?subject=artificial_intelligence",
                200
            )
            
            return success and success2 and success3 and success4
        
        return False

    def test_get_lesson_detail(self):
        """Test getting a single lesson detail"""
        # First get a lesson ID
        success, response = self.run_test(
            "Get Lessons for Detail Test",
            "GET",
            "api/lessons?limit=1",
            200
        )
        
        if success and 'lessons' in response and len(response['lessons']) > 0:
            lesson_id = response['lessons'][0]['id']
            
            success2, response2 = self.run_test(
                "Get Lesson Detail",
                "GET",
                f"api/lessons/{lesson_id}",
                200
            )
            return success2
        
        return False

    def test_quiz_functionality(self):
        """Test quiz endpoints"""
        # Get a lesson with quiz
        success, response = self.run_test(
            "Get Lessons for Quiz Test",
            "GET", 
            "api/lessons?limit=5",
            200
        )
        
        if success and 'lessons' in response:
            for lesson in response['lessons']:
                lesson_id = lesson['id']
                
                # Try to get quiz for this lesson
                success2, quiz_response = self.run_test(
                    f"Get Quiz for Lesson {lesson_id[:8]}",
                    "GET",
                    f"api/quiz/{lesson_id}",
                    200
                )
                
                if success2 and 'questions' in quiz_response:
                    print(f"   📝 Found quiz with {len(quiz_response['questions'])} questions")
                    
                    # Test quiz submission (need authentication)
                    if self.student_token:
                        answers = [0] * len(quiz_response['questions'])  # All first options
                        
                        success3, submit_response = self.run_test(
                            "Submit Quiz",
                            "POST",
                            "api/quiz/submit",
                            200,
                            data={
                                "lesson_id": lesson_id,
                                "user_id": self.student_user_id,
                                "answers": answers
                            },
                            headers={'Authorization': f'Bearer {self.student_token}'}
                        )
                        
                        return success3
                    break
        
        print("   ⚠️  No quizzes found or authentication failed")
        return False

    def test_progress_tracking(self):
        """Test progress tracking endpoints"""
        if not self.student_token or not self.student_user_id:
            print("   ⚠️  Skipping - No student authentication")
            return False
            
        # Test progress update
        success, response = self.run_test(
            "Update Progress",
            "POST",
            "api/progress/update",
            200,
            data={
                "lesson_id": "test-lesson-id",
                "status": "in_progress",
                "time_spent": 15
            },
            headers={'Authorization': f'Bearer {self.student_token}'}
        )
        
        # Test get progress
        success2, response2 = self.run_test(
            "Get User Progress",
            "GET",
            f"api/progress/{self.student_user_id}",
            200,
            headers={'Authorization': f'Bearer {self.student_token}'}
        )
        
        return success and success2

    def test_stats_endpoint(self):
        """Test statistics endpoint"""
        if not self.student_token:
            print("   ⚠️  Skipping - No student authentication")
            return False
            
        success, response = self.run_test(
            "Get User Statistics",
            "GET",
            "api/stats",
            200,
            headers={'Authorization': f'Bearer {self.student_token}'}
        )
        
        if success:
            expected_keys = ['total_lessons', 'completed_lessons', 'in_progress_lessons', 'average_quiz_score']
            for key in expected_keys:
                if key not in response:
                    print(f"   ❌ Missing key: {key}")
                    return False
            print(f"   📊 Stats: {response}")
        
        return success

    def test_inquiry_functionality(self):
        """Test inquiry creation and admin management"""
        # Test creating inquiry (no auth needed)
        success, response = self.run_test(
            "Create Inquiry",
            "POST",
            "api/inquiries",
            200,
            data={
                "name": "Test User",
                "email": "test@example.com",
                "organization": "Test School", 
                "curriculum": "cambridge",
                "grade_range": "5-8",
                "num_students": 30,
                "message": "We are interested in your platform for our students."
            }
        )
        
        if success and 'id' in response:
            self.test_inquiry_id = response['id']
        
        # Test admin getting inquiries
        if self.admin_token:
            success2, response2 = self.run_test(
                "Admin Get Inquiries",
                "GET", 
                "api/admin/inquiries",
                200,
                headers={'Authorization': f'Bearer {self.admin_token}'}
            )
            
            return success and success2
        
        return success

    def test_admin_lesson_crud(self):
        """Test admin lesson CRUD operations"""
        if not self.admin_token:
            print("   ⚠️  Skipping - No admin authentication")
            return False
            
        # Create lesson
        lesson_data = {
            "title": {"en": "Test Lesson", "local": "टेस्ट पाठ"},
            "description": {"en": "A test lesson", "local": "एक टेस्ट पाठ"},
            "content": {"en": "This is test content", "local": "यह टेस्ट सामग्री है"},
            "curriculum": "cambridge",
            "subject": "mathematics", 
            "grade": 5,
            "term": 1,
            "week": 1,
            "language_code": "hi-IN",
            "difficulty": "easy",
            "estimated_duration": 25,
            "source": "Test Source",
            "license": "CC BY 4.0"
        }
        
        success, response = self.run_test(
            "Admin Create Lesson",
            "POST",
            "api/lessons",
            200,
            data=lesson_data,
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        if success and 'id' in response:
            self.created_lesson_id = response['id']
            
            # Test update lesson
            lesson_data['title']['en'] = "Updated Test Lesson"
            success2, response2 = self.run_test(
                "Admin Update Lesson",
                "PUT",
                f"api/lessons/{self.created_lesson_id}",
                200,
                data=lesson_data,
                headers={'Authorization': f'Bearer {self.admin_token}'}
            )
            
            return success2
        
        return False

    def test_sinhala_translations(self):
        """Test Sinhala language translations completeness"""
        # Get AI-STEAM lessons to check translations
        success, response = self.run_test(
            "Get AI-STEAM Lessons for Translation Check",
            "GET",
            "api/lessons?curriculum=AI-STEAM&limit=20",
            200
        )
        
        if success and 'lessons' in response:
            lessons = response['lessons']
            print(f"   🔍 Checking {len(lessons)} lessons for Sinhala translations")
            
            total_checked = 0
            sinhala_title_count = 0
            sinhala_description_count = 0
            sinhala_content_count = 0
            incomplete_translations = []
            
            for lesson in lessons:
                total_checked += 1
                lesson_id = lesson.get('id', 'unknown')[:8]
                
                # Check title translation
                if lesson.get('title', {}).get('si'):
                    sinhala_title_count += 1
                    title_length = len(lesson['title']['si'])
                    if title_length < 5:  # Very short, likely incomplete
                        incomplete_translations.append(f"Lesson {lesson_id}: Short title ({title_length} chars)")
                
                # Check description translation  
                if lesson.get('description', {}).get('si'):
                    sinhala_description_count += 1
                    desc_length = len(lesson['description']['si'])
                    if desc_length < 20:  # Very short description
                        incomplete_translations.append(f"Lesson {lesson_id}: Short description ({desc_length} chars)")
                
                # Check content translation
                if lesson.get('content', {}).get('si'):
                    sinhala_content_count += 1
                    content_length = len(lesson['content']['si'])
                    if content_length < 100:  # Very short content
                        incomplete_translations.append(f"Lesson {lesson_id}: Short content ({content_length} chars)")
            
            print(f"   📊 Translation Coverage:")
            print(f"      Sinhala Titles: {sinhala_title_count}/{total_checked} ({sinhala_title_count/total_checked*100:.1f}%)")
            print(f"      Sinhala Descriptions: {sinhala_description_count}/{total_checked} ({sinhala_description_count/total_checked*100:.1f}%)")
            print(f"      Sinhala Content: {sinhala_content_count}/{total_checked} ({sinhala_content_count/total_checked*100:.1f}%)")
            
            if incomplete_translations:
                print(f"   ⚠️ Potential incomplete translations:")
                for issue in incomplete_translations[:5]:  # Show first 5
                    print(f"      {issue}")
            
            # Consider success if at least 80% have Sinhala translations
            success_rate = min(sinhala_title_count, sinhala_description_count, sinhala_content_count) / total_checked
            return success_rate >= 0.8
        
        return False

    def test_lesson_pdf_download(self):
        """Test lesson PDF download functionality"""
        # Get a lesson ID first
        success, response = self.run_test(
            "Get Lessons for PDF Test",
            "GET",
            "api/lessons?limit=1",
            200
        )
        
        if success and 'lessons' in response and len(response['lessons']) > 0:
            lesson_id = response['lessons'][0]['id']
            
            # Test PDF download (should return binary content)
            success2, _ = self.run_test(
                "Download Lesson PDF",
                "GET",
                f"api/lessons/{lesson_id}/download",
                200
            )
            return success2
        
        return False

    def cleanup_test_data(self):
        """Clean up test data"""
        if self.admin_token and self.created_lesson_id:
            self.run_test(
                "Delete Test Lesson",
                "DELETE",
                f"api/lessons/{self.created_lesson_id}",
                200,
                headers={'Authorization': f'Bearer {self.admin_token}'}
            )

def main():
    print("🚀 Starting Global STEAM Education Hub Backend API Tests")
    print("=" * 60)
    
    tester = GlobalSTEAMHubTester()
    
    # Core API Tests
    tests = [
        ("Health Check", tester.test_health_check),
        ("Student Registration", tester.test_student_registration),
        ("Admin Registration", tester.test_admin_registration), 
        ("Student Login", tester.test_student_login),
        ("Admin Login", tester.test_admin_login),
        ("Get Lessons & Filters", tester.test_get_lessons),
        ("Sinhala Translation Completeness", tester.test_sinhala_translations),
        ("Lesson Detail", tester.test_get_lesson_detail),
        ("Lesson PDF Download", tester.test_lesson_pdf_download),
        ("Quiz Functionality", tester.test_quiz_functionality),
        ("Progress Tracking", tester.test_progress_tracking),
        ("User Statistics", tester.test_stats_endpoint),
        ("Inquiry System", tester.test_inquiry_functionality),
        ("Admin Lesson CRUD", tester.test_admin_lesson_crud),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            results[test_name] = False
    
    # Cleanup
    print(f"\n{'='*20} Cleanup {'='*20}")
    tester.cleanup_test_data()
    
    # Print Results
    print(f"\n{'='*60}")
    print("📊 FINAL TEST RESULTS")
    print(f"{'='*60}")
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    print("\n📋 Test Summary:")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    failed_tests = [name for name, passed in results.items() if not passed]
    if failed_tests:
        print(f"\n⚠️  Failed Tests: {', '.join(failed_tests)}")
        return 1
    else:
        print(f"\n🎉 All backend API tests passed!")
        return 0

if __name__ == "__main__":
    sys.exit(main())