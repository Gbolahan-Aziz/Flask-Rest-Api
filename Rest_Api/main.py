from ctypes import resize
from tkinter import dnd
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class DeptModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gp = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Dept(name = {name}, age = {age}, gp = {gp}, gender = {gender})"
    

dept_put_args = reqparse.RequestParser()
dept_put_args.add_argument("name", type=str, help="Student name is required", required=True)
dept_put_args.add_argument("age", type=int, help="Student age is required", required=True)
dept_put_args.add_argument("gp", type=int, help="Student current grade point average is required", required=True)
dept_put_args.add_argument("gender", type=str, help="Student gender is required", required=True)

dept_update_args = reqparse.RequestParser()
dept_update_args.add_argument("name", type=str, help="Student name is required")
dept_update_args.add_argument("age", type=int, help="Student age is required")
dept_update_args.add_argument("gp", type=int, help="Student current grade point average is required")
dept_update_args.add_argument("gender", type=str, help="Student gender is required")


resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'age': fields.Integer,
	'gp': fields.Integer,
    'gender': fields.String
}
# schema {name,age,gp,gender}
#db.create_all()
class Department(Resource):
    @marshal_with(resource_fields)
    def get(self,student_ID):
        result = DeptModel.query.filter_by(id=student_ID).first()
        if not result:
            abort(404, message="Could not find student with that id")

        return result

    @marshal_with(resource_fields)
    def put(self,student_ID):
        args =  dept_put_args.parse_args()
        result = DeptModel.query.filter_by(id=student_ID).first()
        if result:
            abort(409, message=" Matriculation number has been taken...")
        student =  DeptModel(id=student_ID, name=args['name'], age=args['age'], gp=args['gp'], gender= args['gender'])
        
        db.session.add(student)
        db.session.commit()
        return student, 201


    @marshal_with(resource_fields)
    def patch(self,student_ID):
        args = dept_update_args.parse_args()
        result = DeptModel.query.filter_by(id=student_ID).first()
        if not result:
            abort(404, message="Student data doesn't exist, cannot update")
        
        if args['name']:
            result.name = args['name']
        
        if args['age']:
            result.age = args['age']

        if args['gp']:
            result.gp = args['gp']

        if args['gender']:
            result.gender = args['gender']

        db.session.commit()

        return result


    @marshal_with(resource_fields)
    def delete(self,student_ID):
        result = DeptModel.query.filter_by(id=student_ID).first()

        if not result:
            abort(404, message="Student data doesn't exist, cannot delete")
        db.session.delete(result)
        db.session.commit()



api.add_resource(Department, "/department/<int:student_ID>")

if __name__ == "__main__":
	app.run(debug=True)
