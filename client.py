"""Test code.
"""
import model

# users = [model.User('268339', _following_users=False, _review_list=True),
#          model.User('161540', _following_users=False, _review_list=True),
#          model.User('820000', _following_users=False, _review_list=True)]
users = [model.User('268339', _all=True),
         model.User('161540', _all=True),
         model.User('820000', _all=True)]

for user in users:
    print('')
    print(user.id)
    print(user.name)
    print(user.novels)
    print(user.blogs)
    print(user.bookmarks)
    print(user.following_users)
    print(user.commented_novels)
    print(user.reviews)
