import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it
import time


def LogIn():
    ###############################
    while True:
        ans = input("Are you a registered user? (y/n) Enter \'exit\' to exit: ")
        ans = ans.upper()
        if ans == 'Y':
            while True:
                uid = input("usr is:")
                while True:
                    try:
                        uid = int(uid)
                        break
                    except:
                        uid = input("Wrong input,try again: ")
                
                
                
                
                ups = input("pwd is:")
                ##########
                state = ("select * from users u where u.usr= " + str(uid) + " and u.pwd= \'"+ str(ups) + "\'")
                curs.execute(state)
                rows = curs.fetchall()
                if len(rows) == 1:
                    print("Successfully Login")
                    break
                else:
                    print("Wrong user id or password, try again ")
    
            tweets_retweets(uid)
        
        ###########
        
        elif ans == 'N':
            print("Not registered")
            # get a list of existing Uids
            
            largest = 0
            state = ("select usr from users")
            curs.execute(state)
            rows = curs.fetchall()
            #Uids=[]
            for row in rows:
                if row[0] > largest:
                    largest = row[0]
            new_uid = largest+1
            
            # get new user information
            name = input("What's your name? ")
            while len(name) > 20:
                name = input("name too long, try again ")
            email = input("Your email address is: ")
            while len(email) > 15:
                email = input("email too long, try again ")
            city = input("Your city is: ")
            while len(city) > 12:
                city = input("city too long, try again ")
            timezone = input("Your timezone is: ")
            while True:
                try:
                    timezone = float(timezone)
                    break
                except ValueError:
                    timezone = input("timezone should be a float, try again ")
        
            password = input("Create your password (no more than 4 characters): ")
            while len(password) > 4:
                password = input("password too long, try again ")

            curs.execute("insert into users(usr, pwd, name, email, city, timezone) VALUES ("+ str(new_uid)+ ",\'" + str(password)+ "\', \'" + str(name) +"\',\'" + str(city)+  "\',\'" + str(email) +"\',\'" + str(timezone) +"\')")
            curs.execute("commit")
            uid = new_uid
            print('Successfully registered! Your user id is ' + str(uid) + ' Welcome to Tweet!')
            
            tweets_retweets(uid)
        
        elif ans == 'EXIT':
            break

    else:
        print("Invalid answer,try again")

###################################################################################################

def tweets_retweets(uid):
    state = ("select tid, writer, to_char(tdate), text, replyto from follows f, tweets t where t.writer = f.flwee and f.flwer = " + str(uid) + "order by tdate DESC")
    curs.execute(state)
    tweets = curs.fetchall()
    
    t_r = 0
    more = list_nterms(tweets, t_r, 5)  # jth
    
    choice = input("\nMore actions: \n1. More tweets\n2. One tweet information\n3. Search for tweets\n4. Search for users\n5. Compose a tweet\n6. List followers\n7. Manage lists\n8. Logout: ")
    while True:
        try:
            choice = int(choice)
            break
        except:
            choice = input("Wrong input,try again: ")

    while choice != 8:
        if choice == 1:
            if more:
                t_r = t_r + 5
                more = list_nterms(tweets, t_r, 5)
            else:
                print("\n   No more tweets")

    ##############################################

        elif choice == 2:
            exist = False
            stweet = input("Select a tweet to see more infomation: ")
            while True:
                try:
                    stweet = int(stweet)
                    while not exist:
                        for tweet in tweets:
                            if int(stweet) == tweet[0]:
                                exist = True
                        if not exist:
                            stweet = input("The tid is incorrect, please enter again: ")
                    break
                except:
                    stweet = input("Wrong input,try again: ")




            tweet_info(stweet)
            
            while True:
                rep = input("More action: \n1. Reply\n2. Retweet\n3. Go back\n")
                while True:
                    try:
                        rep = int(rep)
                        break
                    except:
                        rep = input("Wrong input,try again: ")


                if rep == 1:
                    compose(uid, True, int(stweet))
                    break
                elif rep == 2:
                    
                    state = ('insert into retweets values (' + str(uid) + ', ' + str(stweet) + ', sysdate)' )

                    try:
                        curs.execute(state)
                        curs.execute('commit')
                        print("Retweet successfully")
                    except cx_Oracle.DatabaseError:
                        print("You have already retweeted this tweet. ")
            
                    break
                elif rep == 3:
                    break
                else:
                    print("Invalid input,try again: ")

##############################################

        elif choice == 3:
            keywords = input('Please enter keywords, using whitespace to separate: ')
            tresults = search_tweets(keywords)
            
            t_r = 0
            more = list_nterms(tresults, t_r, 5)
            choice = input("\n1. Show more tweets\n2. See more information\n3. Reply\n4. Retweet\n5. Go back: ")
            while True:
                try:
                    choice = int(choice)
                    break
                except:
                    choice = input("Wrong input,try again: ")
        
            while choice != 5:
                if choice == 1:
                    if more:
                        t_r = t_r + 5
                        more = list_nterms(tresults, t_r, 5)
                    else:
                        print("\n   No more tweets")
            
                elif choice == 2:
                    stweet = input('Select a tweet to see more infomation: ')
                  ## check input
                    exist=False
                    
                    while True:
                        try:
                            stweet = int(stweet)
                            while not exist:
                                for tweet in tresults:
                                    if int(stweet) == tweet[0]:
                                        exist = True
                                if not exist:
                                    stweet = input("The tid is incorrect, please enter again: ")
                            break
                        except:
                            stweet = input("Wrong input,try again: ")
                
                
                  ## check input
                    
                    tweet_info(stweet)

                elif choice == 3:
                    tid = input('Select a tweet to reply: ')
                  ## check input
                    exist=False
                    
                    while True:
                        try:
                            tid = int(tid)
                            
                            while not exist:
                                for tweet in tresults:
                                    if int(tid) == tweet[0]:
                                        exist = True
                                if not exist:
                                    tid = input("The tid is incorrect, please enter again: ")
                        
                            break
                        except:
                            tid = input("Wrong input,try again: ")
                
                
                  ## check input
                
                    compose(uid, True, int(tid))


                elif choice == 4:
                    tid = input('Select a tweet to retweet:')
                    exist=False

                  ## check input
                    while True:
                        try:
                            tid = int(tid)
                            while not exist:
                                for tweet in tresults:
                                    if int(tid) == tweet[0]:
                                        exist = True
                                if not exist:
                                    tid = input("The tid is incorrect, please enter again: ")
                            
                            break
                        except:
                            tid = input("Wrong input,try again: ")
            
            
                ## check input
                    
                    state = ('insert into retweets values (' + str(uid) + ', ' + str(tid) + ', sysdate)' )
                    
                    try:
                        curs.execute(state)
                        curs.execute('commit')
                        print("Retweet successful !")
                    except cx_Oracle.DatabaseError:
                        print("You have already retweeted this tweet. ")
                            
                            



                choice = input("\n1. Show more tweets\n2. See more information\n3. Reply\n4. Retweet\n5. Go back: ")
                while True:
                    try:
                        choice = int(choice)
                        break
                    except:
                        choice = input("Wrong input,try again: ")

##############################################

        elif choice == 4:
            keyword = input('Please enter a keyword: ')
            uresults = search_users(keyword)
            
            t_r = 0
            more = list_nterms(uresults, t_r, 5)
            choice = input("\n1. Show more users\n2. See more information of one user\n3. Go back: ")
            while True:
                try:
                    choice = int(choice)
                    break
                except:
                    choice = input("Wrong input,try again: ")
        
            while choice != 3:
                if choice == 1:
                    if more:
                        t_r = t_r + 5
                        more = list_nterms(uresults, t_r, 5)
                    else:
                        print("\n   No more users")
            
                elif choice == 2:
                    selected_uid = input('Select a user id to show: ')
                    exist=False
                    while True:
                        try:
                            selected_uid = int(selected_uid)
                            while not exist:
                                for user in uresults:
                                    if int(selected_uid) == user[0]:
                                        exist = True
                                if not exist:
                                    selected_uid = input("The usr id is incorrect, please enter again: ")
                            
                            break
                        except:
                            selected_uid = input("Wrong input,try again: ")
                    
                    
                    
                    
                    user_info(uid, selected_uid)
                        
                
                choice = input("\n1. Show more users\n2. See more information of one user\n3. Go back: ")
                while True:
                    try:
                        choice = int(choice)
                        break
                    except:
                        choice = input("Wrong input,try again: ")

##############################################

        elif choice == 5:
            compose(uid, False, 1)
        
##############################################
        
        elif choice == 6:
            list_follwes(uid)

##############################################

        elif choice == 7:
            manage_list(uid)
        
##############################################
        
        choice = input("\nMore actions: \n1. More tweets\n2. One tweet information\n3. Search for tweets\n4. Search for users\n5. Compose a tweet\n6. List followers\n7. Manage lists\n8. Logout: ")
        while True:
            try:
                choice = int(choice)
                break
            except:
                choice = input("Wrong input,try again: ")

    print('Logged out successfully.')

###################################################################################################

def tweet_info(stweet):
    
    state = ('select num_ret,  num_rly  from (select count(*) as num_ret from retweets r where r.tid = ' + str(stweet) + '), (select count(*) as num_rly from tweets t where t.replyto = ' + str(stweet) + ')')
    curs.execute(state)
    rows = curs.fetchall()
    print("The number of retweets is: " + str(rows[0][0]))
    print("The number of replies is: " + str(rows[0][1]))

###################################################################################################

def user_info(uid, selected_uid):
    state = ("select count(*) from tweets t where t.writer = " + str(selected_uid))
    curs.execute(state)
    rows = curs.fetchall()
    print("The number of tweets is:" + str(rows[0][0]))
    
    state = ("select count(*) from follows f where f.flwer = " + str(selected_uid))
    curs.execute(state)
    rows = curs.fetchall()
    print("The number of users being followed is:" + str(rows[0][0]))
    
    state = ("select count(*) from follows f where f.flwee = " + str(selected_uid))
    curs.execute(state)
    rows = curs.fetchall()
    print("The number of followers is:" + str(rows[0][0]))
    
    state = ("select tid, writer, to_char(tdate), text, replyto from tweets t where t.writer = " + str(selected_uid) + "order by tdate DESC")
    curs.execute(state)
    rows = curs.fetchall()
    
    t_r = 0
    more = list_nterms(rows, t_r, 3)  # jth
    choice = input("\n1. Follow this guy\n2. Show more tweets\n3. Go back: ")
    while True:
        try:
            choice = int(choice)
            break
        except:
            choice = input("Wrong input,try again: ")

    while choice != 3:
        if choice == 1:
            if uid != selected_uid:
                try:
                    curs.execute('insert into follows values ('+ str(uid) + ', ' + str(selected_uid) + ', sysdate)')
                    curs.execute('commit')
                    print('You followed him/her successfully! ')
                except cx_Oracle.DatabaseError:
                    print("You have already followed him/her. ")
            else:
                print('Sorry, you cannot follow yourself.')

        elif choice == 2:
            if more:
                t_r = t_r + 3
                more = list_nterms(rows, t_r, 3)  # jth
            else:
                print("\n   No more tweets")

        choice = input("\n1. Follow this guy\n2. Show more tweets\n3. Go back: ")
        while True:
            try:
                choice = int(choice)
                break
            except:
                choice = input("Wrong input,try again: ")


###################################################################################################

def compose(uid, reply, reply_to): # input: (int: writer's uid, bool: if this is a reply, int: replied tid)
    # get a list of existing tids
    largest = 0
    state = ("select tid from tweets")
    curs.execute(state)
    rows = curs.fetchall()
    #Tids=[]
    for row in rows:
        if row[0] > largest:
            largest = row[0]
    new_tid = largest+1
    
    # input text and find hashtags
    long_text = True
    long_hashtag = True
    
    while long_text or long_hashtag:
        long_text = False
        long_hashtag = False
        
        text = input("Please text your tweet: ")
        if len(text) > 80:
            long_text = True
    
        words = text.split(' ')
        hashtags = []
        
        for word in words:
            if word[0] == '#':
                word = word[1:] # delete # from this word
                if word[-1].isalpha() == False and word[-1].isdigit() == False:
                    word = word[:-1] # delete symbol if there is a symbol at the end of the word
                
                if len(word) > 10:
                    print('Hashtag is longer than 10 letters! Please text tweet again.')
                    long_hashtag = True
                    break
                elif word != '':
                    hashtags.append(word) # append this word as hashtag into hashtags list, if the word is not empty (avoid for enter empty hashtag)

    # insert tweet to tweets
    state = ('insert into tweets values (' + str(new_tid) + ', ' + str(uid) + ', sysdate,\''  + text + '\', ')
    if reply:
        state = state + str(reply_to) + ')'
    else:
        state = state + 'null)'

    curs.execute(state)
    
    # insert hashtags to hashtags and mentions
    state = ("select trim(term) from hashtags")
    curs.execute(state)
    rows = curs.fetchall()
    
    ex_hashtags = []
    for row in rows:
        ex_hashtags.append(row[0])
    
    for hashtag in hashtags:
        if hashtag not in ex_hashtags:
            curs.execute('insert into hashtags values (\'' + hashtag + '\')')
        curs.execute('insert into mentions values ('+ str(new_tid)+ ',\'' + hashtag +'\')')
    
    curs.execute('commit')
    print('Tweet successfully!')

###################################################################################################

def list_follwes(uid):
    state = ("select flwer from follows f where f.flwee = " + str(uid))
    curs.execute(state)
    rows = curs.fetchall()
    
    print("Your followers are: ")
    for row in rows:
        print(row[0])
    
    exist = False
    flwer = input("More information about one follower: ")
    while True:
        try:
            flwer = int(flwer)
            while not exist:
                for i in range(0,len(rows)):
                    if int(flwer) == rows[i][0]:
                        exist= True
                if not exist:
                    flwer = input("Follower not exist, try again: ")
        
            break
        except:
            flwer = input("Wrong input,try again: ")



    user_info(uid, flwer)

###################################################################################################

def list_nterms(rows, jth, num_t):
    num = len(rows)
    i = 0
    if jth + num_t >= num :     # less than or equal to num_t tweets left
        while i < (num - jth):
            print(rows[i + jth])
            i = i + 1
        return False                # this means no more tweets
    else:
        while i < num_t:
            print(rows[i + jth])
            i = i + 1
        return True                 # we still have some tweets

###################################################################################################

def search_tweets(words): # input: keywords ; return: search result as list
    keywords = words.split(' ')
    
    state = ('select tid, writer, to_char(tdate), text, replyto from tweets left outer join mentions using (tid) where ')
    
    for keyword in keywords:
        if keyword[0] == '#': # if the keyword is a hashtag keyword, add where statement which search for mentions
            keyword = keyword[1:]
            where = 'upper(term)= \'' + keyword.upper() + '\' '
        else: # else just search for text
            where = 'upper(text) like \'%' + keyword.upper() + '%\' '
        
        state = state + where + 'or '
    
    state = state[:-3] # delete the last or at the end
    state = state + 'order by tdate desc'

    print(state)

    curs.execute(state)
    rows = curs.fetchall()
    return rows


###################################################################################################

def search_users(keyword): # input keyword ; return: search result as list
    state = ('select usr, name, email, city, timezone from users where upper(name) like \'%' + str(keyword).upper() + '%\' order by length(trim(name))')
    curs.execute(state)
    rows = curs.fetchall()
    
    state = ('select usr, name, email, city, timezone from (select * from users where upper(city) like \'%' + str(keyword).upper() + '%\' minus select * from users where upper(name) like \'%' + str(keyword).upper() + '%\') order by length(trim(city))')
    curs.execute(state)
    
    rows=rows+curs.fetchall()
    #rows.append(curs.fetchall())
    
    #print(rows)
    
    return rows

###################################################################################################

def manage_list(uid):
    choice = input('Please choose your action: \n' +
                   'a. Get a listing of your lists \n' +
                   'b. See the lists that you are on \n' +
                   'c. Create a list \n' +
                   'd. Add a member to your list \n' +
                   'e. Delete a member from your list \n' +
                   'f. Back to menu \n' +
                   'Plese enter your choice: ').upper()
        
    while choice != 'F':
        if choice == 'A':
            get_list(uid)
        elif choice == 'B':
            see_list_enrolled(uid)
        elif choice == 'C':
            create_list(uid)
        elif choice == 'D':
            add_members(uid)
        elif choice == 'E':
            delete_member(uid)
                
        choice = input('\nPlease choose your action: \n' +
                        'a. Get a listing of your lists \n' +
                        'b. See the lists that you are on \n' +
                        'c. Create a list \n' +
                        'd. Add a member to your list \n' +
                        'e. Delete a member from your list \n' +
                        'f. Back to menu \n' +
                        'Plese enter your choice: ').upper()
###################################################################################################


def get_list(uid):
    state = ('select * from lists where owner = ' + str(uid))
    curs.execute(state)
    rows = curs.fetchall()
    
    for row in rows:
        print(row[0] + '\n')

###################################################################################################

def see_list_enrolled(uid):
    state = ('select * from includes where member = ' + str(uid))
    curs.execute(state)
    rows = curs.fetchall()
    
    for row in rows:
        print(row[0] + '\n')

###################################################################################################

def create_list(uid):
    lname_not_exist = True
    
    while (lname_not_exist):
        lname = input('\nPlease enter the name of list: ')
        state = ('select * from lists where lname = \'' + str(lname) + '\'')
        curs.execute(state)
        rows = curs.fetchall()
        
        if rows == []: # result is empty, or there is not any list has same name with lname
            lname_not_exist = False
        else:
            print('\nList name exists, please use other list names.')
    
    state = ('insert into lists values(\'' + str(lname) + '\', ' + str(uid) +')')
    curs.execute(state)
    curs.execute('commit')
    print('\nList create successfully.')

###################################################################################################

def add_members(uid):
    exist = True
    
    state = ("select usr from users")
    curs.execute(state)
    users = curs.fetchall()
    
    
    while exist:
        add_uid = input('\nPlease enter the user id you want to add in: ')
        in_data=False
        while True:
            try:
                int(add_uid)
                
                while not in_data:
                    for user in users:
                        if int(add_uid) == user[0]:
                            in_data = True
                    if not in_data:
                        add_uid = input("The user does not exist, please enter again: ")
                
                break
            except:
                add_uid = input("Wrong input,try again: ")


    
    
    
    
    
        lname = input('Please enter the list name you want to add the member in : ')
        
        # check whether the user is the owner of the list
        state = ('select * from lists where lname = \'' + lname + '\' and owner = ' + str(uid))
        curs.execute(state)
        rows = curs.fetchall()
        if rows == []:
            print('\nSorry, you are not the owner of this list.')
        else:
            # check whether the add_uid is already in the member of the list
            state = ('select * from includes where lname = \'' + lname + '\' and member = ' + add_uid)
            curs.execute(state)
            rows = curs.fetchall()
            #print('List name or user id not existing.')
            
            if rows == []:
                exist = False
                state = ('insert into includes values (\'' + lname + '\', ' + add_uid + ')')
                curs.execute(state)
                curs.execute('commit')
                print('\nSuccessfully added')
            else:
                print('\nMember exists.')


###################################################################################################

def delete_member(uid):
    state = ('select i.lname as lname, i.member as member from lists l, includes i where l.lname = i.lname and l.owner = ' + str(uid))
    curs.execute(state)
    rows = curs.fetchall()
    
    for row in rows:
        print(row)

    exist = False

    while not exist:
        lname = input('\nPlease enter the list name you want to delete member from: ')
        del_uid = input('Plese enter the user id you want to delete from the list: ')
        while True:
            try:
                int(del_uid)
                break
            except:
                del_uid = input("Wrong input,try again: ")

        
        # check whether the user is the owner of the list
        state = ('select * from lists where lname = \'' + lname + '\' and owner = ' + str(uid))
        curs.execute(state)
        rows = curs.fetchall()
        if rows == []:
            print('\nSorry, you are not the owner of this list.')
        else:
            # check whether the del_uid is not exist in the member of the list
            state = ('select * from includes where lname = \'' + lname + '\' and member = ' + del_uid)
            curs.execute(state)
            rows = curs.fetchall()
            
            if rows != []:
                exist = True
                state = ('delete from includes where lname = \'' + lname + '\' and member = ' + del_uid)
                curs.execute(state)
                curs.execute('commit')
                print('\nSuccessfully delected')

            else:
                print('\nMember not exists.')


###################################################################################################




if __name__ == "__main__":
    # get username
    user = input("Username [%s]: " % getpass.getuser())
    
    if not user:
        user = getpass.getuser()
    
    # get password
    pw = getpass.getpass()
    
    # The URL we are connnecting to
    conString = '' + user + '/' + pw + '@gwynne.cs.ualberta.ca:1521/CRS'
    # SQL statement to execute
    #createStr = ("@prj-tables")
    try:
        # Establish a connection in Python
        connection = cx_Oracle.connect(conString)
        # create a cursor
        curs = connection.cursor()
        
        ##################
        
        uid = LogIn()
        
        ##############
        
        # close the connection
        curs.close()
        connection.close()
        exit()
    
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print( sys.stderr, "Oracle code:", error.code)
        print( sys.stderr, "Oracle message:", error.message)




