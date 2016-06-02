"""Test code.
"""
import model

users = [model.User('268339', _following_users=False, _review_list=True),
         model.User('161540', _following_users=False, _review_list=True),
         model.User('820000', _following_users=False, _review_list=True)]
users = [model.User('268339'),
         model.User('161540'),
         model.User('820000')]

for user in users:
    user.init(_all=True)

    print('')
    print(user.id)
    print(user.name)
    print(user.novels)
    print(user.blogs)
    print(user.bookmarks)
    print(user.following_users)
    print(user.commented_novels)
    print(user.reviews)

novel = model.Novel('n3311bu')
novel.get_info()

print(novel.id)
print(novel.title)
print(novel.user_id)
print(novel.category)
print(novel.publication_date)
print(novel.last_date)
print(novel.impression_count)
print(novel.review_count)
print(novel.bookmark_count)
print(novel.assessment)
print(novel.point_writing)
print(novel.point_story)
print(novel.chara_count)
