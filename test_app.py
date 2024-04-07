from unittest import TestCase
from models import db, User
from app import app


# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']






class ViewsTestCase(TestCase):
    def setUp(self):
        self.app = app.test_client()  # Create a test client for the Flask app
        self.ctx = app.app_context()
        self.ctx.push()  # Push the application context
        db.drop_all()
        db.create_all()
        """Add sample pet."""
        user = User(first_name="Nihal", last_name = "Chehade", image_url= "")
       
        db.session.add(user)
        db.session.commit()
        # Create any test data or perform setup here

    def tearDown(self):
        db.session.rollback()  # Remove the database session
        self.ctx.pop()  # Pop the application context


    def test_list_users(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('Nihal Chehade', html)


    def test_add_user(self):
         with app.test_client() as client:
            data_dic = {'firstName':'Ayla', 'lastName':'Alloushe', 'imgUrl':''}
            res = client.post('/users/new', data=data_dic)
                        
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users')

    def test_redirect(self):
        with app.test_client() as client:
            res = client.get('/')
            
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users')

    def test_redirect_followed(self):
        with app.test_client() as client:
            res = client.get('/', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>All Users:</h1>', html)