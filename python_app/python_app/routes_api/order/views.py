from pyramid.view import view_config
from python_app.db.order import Order
from python_app import db
from sqlalchemy.orm import Session
from pyramid.httpexceptions import HTTPBadRequest
from sqlalchemy import select

class OrderView(object):
    def __init__(self, request):
        self.request = request

        
    @view_config(route_name="order_root", request_method="POST", renderer='json')
    def order(self):
        body = self.request.json_body
        name_in = body.get('name')
        email_in = body.get('email')
        if email_in and name_in:     
            with Session(db.open(self.request.registry.settings)) as session:
                order = Order(
                    name=name_in,
                    email=email_in
                    )
                session.add(order)
                session.commit()
                return order.to_dict()
        else:
            raise HTTPBadRequest()
        return "OK"
    
    @view_config(route_name="order_assessment", request_method="GET", renderer='json')
    def order_get(self):
        id = self.request.matchdict.get("order_id")
        with Session(db.open(self.request.registry.settings)) as session:
            order = session.execute(
                select(Order).
                filter(Order.id == id)
            ).scalar_one_or_none()
            if order and order.status != "Redacted":
                return order.to_dict()
            else:
                self.request.response.status_code = 404
                return f"Order id:{id} not found"  

    @view_config(route_name="order_assessment", request_method="DELETE", renderer='json')
    def delete_order(self):
        id = self.request.matchdict.get("order_id")
        with Session(db.open(self.request.registry.settings)) as session:
            order = session.execute(
                select(Order).
                filter(Order.id == id)
            ).scalar_one_or_none()
            if order:
                if order.status == "Completed":
                    return self.request.response
                else:
                    order.status = "Redacted"
                    session.flush()
                    session.commit() 
            else:
                self.request.response.status_code = 404
                return f"Order id:{id} not found"          
        
    @view_config(route_name="order_assessment", request_method="POST", renderer='json')
    def take_assessment(self):
        id = self.request.matchdict.get("order_id")
        with Session(db.open(self.request.registry.settings)) as session:
            order = session.execute(
                select(Order).
                filter(Order.id == id)
            ).scalar_one_or_none()
            if order:
                if not order.status:
                    order.status = "Completed"
                    session.flush()
                    session.commit()
                elif order.status == "Redacted":
                    self.request.response.status_code = 410
                    self.request.response.text = 'Redacted' 
                    return self.request.response
                else:
                    self.request.response.status_code = 410
                    self.request.response.text = 'Already Completed'
                    return self.request.response
            else:
                self.request.response.status_code = 404
                return f"Order id:{id} not found"

            return order.to_dict()
