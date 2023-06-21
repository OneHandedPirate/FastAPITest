import datetime
from random import randint

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models, schemas, utils, oauth2
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/', status_code=status.HTTP_200_OK)
def root():
    return {"Welcome to TestAPI by OneHandedPirate. The following paths are available": ['create_account', 'login', 'get_info', 'delete_account']}

@app.post('/create_account', status_code=status.HTTP_201_CREATED,
          response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(models.User).filter_by(username=user.username).first()

    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'The user {user.username} is already registered')

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user_dict = user.dict()
    new_user = models.User(**new_user_dict)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_employee_obj = models.Employee(salary=randint(10000, 100000),
                                       user_id=new_user.id,
                                       promotion_date=datetime.datetime.now()
                                                      + datetime.timedelta(days=randint(10, 1000)))
    db.add(new_employee_obj)
    db.commit()

    return new_user


@app.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):

    # OAuth2PasswordRequestForm expects username instead of login field
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid credentials')

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid credentials')

    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {"access_token": access_token, 'token_type': "bearer"}


@app.get("/get_info", response_model=schemas.EmployeeResponse)
def get_info(db: Session = Depends(get_db),
             current_user: models.User = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Probably the employee was fired")

    employee_info = db.query(models.Employee).filter(models.Employee.user_id == current_user.id).first()

    return employee_info


@app.delete("/delete_account/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User {username} does not exist')

    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
