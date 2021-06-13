from userUtil import confirm_user_exists

existsUser = 'testUser'
notExistsUser = 'doesntexist'
print(confirm_user_exists(existsUser), "should be True")
print(confirm_user_exists(notExistsUser), "should be False")