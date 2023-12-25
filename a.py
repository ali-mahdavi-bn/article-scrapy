from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    hashed_password = Column(String)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./identifier.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

from sqlalchemy import event,delete
from sqlalchemy.orm import Session


@event.listens_for(Session, 'do_orm_execute')
def receive_do_orm_execute(orm_execute_state):
    print('Executing ORM statement: ', orm_execute_state.statement)
    print('Parameters: ', orm_execute_state.params)


from fastapi import FastAPI, Depends

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/")
def create_user(db: Session = Depends(get_db)):
    user = User()
    user.name = "ali"
    user.email = "a@a.com"
    # delete_stmt = db.execute(delete(User).where(User.id == 1))
    # a=db.query(User).filter(User.id==2).all()
    # db.commit()
    db.add(user)
    db.commit()
    return {"a", "b"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('a:app', host="0.0.0.0", port=8000)
