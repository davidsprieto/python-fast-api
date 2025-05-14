from pydantic import BaseModel


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int


class CommentIn(BaseModel):
    body: str
    # post_id: int ## commented out because the post_id will come as a query parameter, not in the body of the post request.


class Comment(CommentIn):
    id: int


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]


