from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from config.database import get_db
from dto.orderschema import OrderCreatePlaceOrder
from .orderservice import OrderService

router = APIRouter(prefix="/order", tags=["Order"])


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return OrderService.getAll(db=db)


@router.post("/")
def create_order(request: OrderCreatePlaceOrder, db: Session = Depends(get_db)):
    return OrderService.createOrderPlace(request=request, db=db)


@router.get("/orderbyuser/{userid}")
def order_by_user(userid: int, db: Session = Depends(get_db)):
    return OrderService.getOrderByUserId(userid=userid, db=db)


@router.get("/orderbyid/{id}")
def order_by_id(id: int, db: Session = Depends(get_db)):
    return OrderService.getOrderById(id=id, db=db)


# @router.get("/export-csv")
# def export_csv(db: Session = Depends(get_db)):
#     orders = OrderService.getAll(db=db)
#
#     csv_data = "OrderID,Product,Quantity,Price,Name,Email,TransactionId,UserId,Id,IsDelivered\n"
#     for order in orders:
#         csv_data += f"{order.id},{order.name},{order.orderAmount},{order.price},"
#         csv_data += f"{order.name},{order.email},{order.transactionId},{order.user_id},{order.id},{order.isDelivered}\n"
#
#     # Membuat respons StreamingResponse dengan tipe konten CSV
#     response = StreamingResponse(content=iter([csv_data]), media_type="text/csv")
#     response.headers["Content-Disposition"] = 'attachment; filename="orders.csv"'
#
#     return response
