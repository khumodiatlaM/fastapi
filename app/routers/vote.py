from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Votes"],
    # dependencies=[Depends(oauth2.get_current_user)],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vote(vote: schemas.VoteCreate, 
                      db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id:{vote.post_id} not found")
  
    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    
    if vote.vote_dir == 1:
        if vote_query.first(): 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail= f"User with id:{current_user.id} has already voted for this post")
        
        new_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote created successfully"}
    else:
        if not vote_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Vote with id:{vote.post_id} does not exist")
         
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}  

   
    
   
    
    