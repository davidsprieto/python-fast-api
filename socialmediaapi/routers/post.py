from fastapi import APIRouter, HTTPException, Query

from socialmediaapi.models.post import *

router = APIRouter()

post_table = {}
comment_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


@router.post("/posts", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    user_post = post.model_dump()
    last_record_id = len(post_table) + 1
    new_post = {"id": last_record_id, **user_post}
    post_table[last_record_id] = new_post
    return new_post


@router.get("/posts", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())


@router.post("/posts/{post_id}/comments", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn, post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    user_comment = comment.model_dump()
    user_comment['post_id'] = post_id

    last_record_id = len(comment_table) + 1
    new_comment = {"id": last_record_id, **user_comment}
    comment_table[last_record_id] = new_comment
    return new_comment


@router.get("/posts/{post_id}/comments", response_model=list[Comment])
async def get_all_comments_of_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = [comment for comment in comment_table.values() if comment["post_id"] == post_id]

    if not comments:
        raise HTTPException(status_code=404, detail="Comments not found")

    return comments


@router.get("/posts/{post_id}", response_model=UserPostWithComments)
async def get_post_and_all_comments_of_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_all_comments_of_post(post_id)
    }
