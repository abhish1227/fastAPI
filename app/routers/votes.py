from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2


router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(body: schemas.Vote, db: Session = Depends(database.get_db), curr_user: int = Depends(oauth2.get_current_user)):

    find_post = db.query(models.Post).filter(
        models.Post.id == body.post_id).first()
    if not find_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {body.post_id} does not exists.")

    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == body.post_id, models.Votes.user_id == curr_user.id)
    found_vote = vote_query.first()
    if (body.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {curr_user.id} has already voted on the post {body.post_id}.")

        new_vote = models.Votes(post_id=body.post_id, user_id=curr_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote."}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Your vote on this post does not exist.")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote."}
