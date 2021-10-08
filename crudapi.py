from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)
db=SQLAlchemy(app)
ms=Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:@localhost/bookcrudapi"

#class model booking
class Booking(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	city_name = db.Column(db.String(20), nullable=False)
	status = db.Column(db.String(20), nullable=False)  

	def __init__(self,id,city_name,status):
		self.id=id
		self.city_name=city_name
		self.status=status

#schema for  booking 
class BookingSchema(ms.Schema):
	class Meta:
		fields=('id','city_name', 'status')


#objects schema for booking
bookingSchema=BookingSchema()
bookingsSchema=BookingSchema(many=True)

@app.route("/addbooking", methods=['POST'])
def addbooking():
	bookings=request.json["bookings"]
	print(bookings)
	bookingMetaData=request.json["bookingMetaData"]
	print(bookingMetaData)
	if bookings=='Booking':
		newbooking=Booking(bookingMetaData["id"],bookingMetaData["city_name"], bookingMetaData["status"])
		print(newbooking)
		db.session.add(newbooking)
		db.session.commit()
		return jsonify({"action is successfully": "200 ok"}), 200
	else:
		return jsonify({"request is invalid":"404 bad request"}), 400

@app.route('/<string:bookings>/<int:bookingFileId>', methods=['DELETE'])
def deletebooking(bookings,bookingFileId):
	if bookings=='Booking':
		booking=Booking.query.get(bookingFileId)
		db.session.delete(booking)
		db.session.commit()
		return jsonify({"Action is successful": "200 OK"}),200
	else:
		return jsonify({"Request is invalid":"400 bad request"}),400

@app.route('/<string:bookings>/<int:bookingFileId>', methods=['PUT'])
def updatebooking(bookings,bookingFileId):
   bookingMetaData=request.json["bookingMetaData"]
   if bookings=='Booking':
   	    booking=Booking.query.get(bookingFileId)
   	    booking.id=bookingMetaData["id"]
   	    booking.city_name=bookingMetaData["city_name"]
   	    booking.status=bookingMetaData["status"]
   	    db.session.commit()
   	    return jsonify({"Action is successful": "200 OK"}),200
   else:
   	return jsonify({"Request is invalid":"400 bad request"}),400


@app.route('/<string:bookings>',methods=['GET'])
@app.route('/<string:bookings>/<int:bookingFileId>',methods=['GET'])
def GetData(bookings,bookingFileId=0):
    if bookings=='Booking':
        if bookingFileId==0:
            booking=Booking.query.all()
            allbooking=songsSchema.dump(booking)
            return jsonify(allbooking)
        else:
            booking=Booking.query.get(bookingFileId)
            return bookingSchema.jsonify(booking)
    else:
        return jsonify({"Request is invalid":"400 bad request"}),400


if __name__ == '__main__':
	app.run(debug=True)