from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


# @router.get("/", response_model=List[schemas.Vote])
# def get_votes(db: Session = Depends(get_db), 
#               current_user: models.User = Depends(oauth2.get_current_user), 
#               limit: int = 10, 
#               skip: int = 0,
#               search: Optional[str] = ""):
#     # cursor.execute("""SELECT * FROM posts """)
#     # posts = cursor.fetchall()
    
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
#     # .all()
#     # .filter(models.Post.owner_uuid==current_user.uuid)

#     return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_create_vote(
    vote: schemas.Vote, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.uuid==vote.post_uuid).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {vote.post_uuid} does not exist")
    
    vote_guery = db.query(models.Vote).filter(models.Vote.post_uuid == vote.post_uuid, 
                                            models.Vote.user_uuid == current_user.uuid)
    
    found_vote = vote_guery.first()
    
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"user {current_user.uuid} has already voted on post {vote.post_uuid}")
            
        new_vote = models.Vote(post_uuid = vote.post_uuid, user_uuid = current_user.uuid)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfuly added a vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"vote does not exist")
            
        vote_guery.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfuly deleted a vote"}
        

# @router.get("/{id}", response_model=schemas.Post)
# def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#     # cursor.execute("""SELECT * FROM posts WHERE uuid = %s """, (str(id)))
#     # post = cursor.fetchone()
#     post = db.query(models.Post).filter(models.Post.uuid == id).first()
    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} not found") 
    
#     return post


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#     # cursor.execute("""DELETE FROM posts WHERE uuid = %s RETURNING *""", 
#     #                (str(id)))
#     # del_post = cursor.fetchone()
#     # conn.commit()
#     post_query = db.query(models.Post).filter(models.Post.uuid == id)
#     post_record = post_query.first()

#     if not post_record:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} not found")
        
#     if post_record.owner_uuid != current_user.uuid:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail=f"Not authorized to perform requested action")
        
#     post_query.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("/{id}", response_model=schemas.Post)
# def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE uuid = %s RETURNING * """, 
#     #                (post.title, post.content, post.published, str(id)))
#     # updated_post = cursor.fetchone()
#     # conn.commit()
    
#     post_query = db.query(models.Post).filter(models.Post.uuid == id)
#     post_record = post_query.first()

#     if not post_record:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} not found")
        
#     if post_record.owner_uuid != current_user.uuid:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail=f"Not authorized to perform requested action")
        
#     post_query.update(post.model_dump(), synchronize_session=False)
#     db.commit()
        
#     return post_query.first()
