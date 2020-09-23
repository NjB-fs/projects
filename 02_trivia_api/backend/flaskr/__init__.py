import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  

  QUESTIONS_PER_PAGE = 10
  # page = request.args.get('page', 1, type=int)
  # start = (page-1)*QUESTIONS_PER_PAGE
  # end = start + QUESTIONS_PER_PAGE

  # @TODO: 
  # Create an endpoint to handle GET requests 
  # for all available categories.
  
  @app.route('/categories', methods=['GET'])
  def get_categories():
      categories_dict = {category.id: category.type for category in Category.query.order_by(Category.id).all()}
      return jsonify ({
        'categories': categories_dict
        })
      
  # @TODO: 
  # Create an endpoint to handle GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. 

  @app.route('/questions', methods=['GET'])
  def get_questions():
      
      page = request.args.get('page',1, type=int)
      start=(page-1)* QUESTIONS_PER_PAGE
      end=start + QUESTIONS_PER_PAGE
      questions=[question.format() for question in Question.query.all()]
      categories_list = {category.id: category.type for category in Category.query.order_by(Category.id).all()}
      if len(questions) ==0:
        abort(404)
      return jsonify({
        'success': True,
        'questions': questions[start:end],
        'total_questions': len(questions),
        'current_category': None,
        'categories':categories_list,
      })  

  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 

  
  # @TODO: 
  # Create an endpoint to DELETE question using a question ID. 

  @app.route('/questions/<int:question_id>', methods=['GET', 'DELETE'])
  def delete_question(question_id):
      # body = request.get_json()
      question=Question.query.get_or_404(question_id)
      question.delete()
      page = request.args.get('page', 1, type=int)
      start = (page-1)*QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions=[question.format() for question in Question.query.all()]
      return jsonify({
        'success': True,
        'questions': questions[start:end],
        'total_questions': len(questions)
      })


  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page. 
  

  
  # @TODO: 
  # Create an endpoint to POST a new question, 
  # which will require the question and answer text, 
  # category, and difficulty score.

  # TEST: When you submit a question on the "Add" tab, 
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.  
  
  @app.route('/questions', methods=['POST'])
  def add_question():
      body=request.get_json()
      question=body.get('question', None)
      answer=body.get('answer', None)
      difficulty=body.get('difficulty', None)
      category=body('category', None)
      
      try:
        question=Question(question=question, answer=answer, difficulty=difficulty, category=category)
        question.insert()
        print('your question was successfully listed')
        questions = Question.query.order_by(Question.id).all()
        if len(questions)==0:
          abort(404)
          return jsonify({
            'success': True,
            'questions': questions[start:end],
            'total_questions': len(questions),
            'current_category': None,
          })  
      except:
          abort(422)

  
  # @TODO: 
  # Create a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term 
  # is a substring of the question. 

  @app.route('/questions',methods= ['POST'])
  def search_question():
      body = request.get_json()
      searchTerm = body.get('searchTerm',None) 
      search_question = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
      questions = [Question.format() for question in search_question]
      return jsonify({
        'questions': questions,
        'total_questions': len(questions),
        'current_category': None
      })


  # TEST: Search by any phrase. The questions list will update to include 
  # only question that include that string within their question. 
  # Try using the word "title" to start. 
  
  
  
  # @TODO: 
  # Create a GET endpoint to get questions based on category. 

  @app.route('/categories/<int:category_id>/questions',methods= ['GET'])
    def get_questions_by_category(category_id):  
        page = request.args.get('page', 1, type=int)
        start = (page-1) * QUESTIONS_PER_PAGE
        end = page + QUESTIONS_PER_PAGE
        questions = Question.query.filter(Question.category == category_id).all()
        return jsonify({
          'questions': questions[start:end],
          'total_questions': len(questions),
          'category': category_id,
          # 'categories': categories_list
        })


  # TEST: In the "List" tab / main screen, clicking on one of the 
  # categories in the left column will cause only questions of that 
  # category to be shown. 
  
  


  
  # @TODO: 
  # Create a POST endpoint to get questions to play the quiz. 
  # This endpoint should take category and previous question parameters 
  # and return a random questions within the given category, 
  # if provided, and that is not one of the previous questions. 

@app.route('/play',methods= ['POST'])
  
  


  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not. 
  
  
  # @TODO: 
  # Create error handlers for all expected errors 
  # including 404 and 422. 
  
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad request"
      }), 400


  @app.errorhandler(404)
  def resource_not_found(error):
      return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
      }), 404

  @app.errorhandler(405)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method not allowed"
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
      }), 422

  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
      }), 500
  
  return app

    