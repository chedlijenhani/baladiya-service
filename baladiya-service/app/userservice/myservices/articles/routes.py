from flask import request, jsonify, Blueprint, current_app, url_for, make_response
from flask_marshmallow import Marshmallow
from userservice.myservices.articles.models  import Article
from userservice import db, bcrypt, login_manager, app
from flask_login import login_user, current_user, logout_user, login_required
from userservice.myservices.decorators import require_appkey, token_required
from datetime import datetime
from flask_cors import CORS,cross_origin
from flask import send_file, send_from_directory, safe_join, abort
import random ,werkzeug,os,jwt ,base64
#blueprint
article = Blueprint('article', __name__)

# Init marshmallow
ma = Marshmallow(article)

# Article Schema
class ArticleSchema(ma.Schema):
  class Meta:
    fields = ('idArticle','nameArticle','description','imageArticle','dateCreated','dateEnd')

# Init schema
articleschema = ArticleSchema(strict=True)
article_schema = ArticleSchema(many=True, strict=True)

#get all article
@article.route('/Article', methods=['GET'])
#@require_appkey
@cross_origin()
def getArticle():
        all_Article =Article.query.order_by(Article.idArticle.desc())
        result = article_schema.dump(all_Article)
        return jsonify(result.data)

@article.route('/Article/image', methods=['POST'])
@require_appkey
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def setImage():
    now = datetime.now()
    timeStamp = now.strftime("%m/%d/%Y, %H:%M:%S")
    rand = str(int(random.random() * 100000000))
    file = request.files['image']
    imagefile = timeStamp + rand + file.filename
    filename = werkzeug.utils.secure_filename(imagefile)
    file.save(os.path.join("./static/profile_pics", filename))
    nameArticle = request.headers.get('nameArticle')
    imageArticle = filename
    description = request.headers.get('description')
    dateEnd = request.headers.get('dateEnd')
    dateCreated = now.strftime("%d/%m/%Y")
    now = datetime.now()
    dateCreated = now.strftime("%d/%m/%Y")
    new_ART = Article(nameArticle,description,imageArticle,dateCreated,dateEnd)
    db.session.add(new_ART)
    db.session.commit()
    return jsonify({  'check': True ,
    'msg': 'New Article successfully created !',
                      'filename': filename })

@article.route('/Article/getImage', methods=['GET'])
@require_appkey
@cross_origin()
def getImageArticle():
    imageArticle=request.headers.get('image')
    filename = os.path.join('../static/profile_pics/' + imageArticle)
    return send_file(filename, mimetype='image/png')

# Delete user
@article.route('/Article/delete', methods=['DELETE'])
@require_appkey
@cross_origin()
def deleteArticle():
        idArticle = request.json['idArticle']
        # fetch user
        ART = Article.query.filter_by(idArticle=idArticle).first()
        if not ART:
            return jsonify({'msg': 'No ART found !'})
        db.session.delete(ART)
        db.session.commit()
        return jsonify({'msg': 'Article has been deleted !'})
# Create account ADMIN et client web
@article.route('/Article/add', methods=['POST'])
@require_appkey
@cross_origin()
def createArticle():
        nameArticle = request.json['nameArticle']
        imageArticle = request.json['imageArticle']
        description = request.json['description']
        dateEnd = request.json['dateEnd']
        now = datetime.now()
        dateCreated = now.strftime("%d/%m/%Y")
        new_ART = Article(nameArticle,description,imageArticle,dateEnd,dateCreated)
        db.session.add(new_ART)
        db.session.commit()
        return jsonify({
            'check': True ,
            'msg': 'New Article successfully created !'
        })
