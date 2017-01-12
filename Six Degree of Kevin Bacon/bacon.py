#To load the text into a string:
def remove_space(info_string):
    for char in info_string:
        if char=="\t" or char==" ":
            info_string = info_string[1:]
        else:
            break
    return info_string

def create_movie_list(info_string):

    movie_list=[]
    test=[]
    while info_string:
        info_string = remove_space(info_string)
        movie_end = info_string.find(")")
        movie_name = info_string[0:movie_end+1]
        info_string= info_string[info_string.find("\n")+1:]
        if ord(info_string[0:1]) in range(65,122) or movie_end==-1:
            break
        movie_list.append(movie_name)
        
    return info_string, movie_list


def find_name(info_string):    
    lastname_end = info_string.find(",")
    lastname= info_string[0:lastname_end]
    info_string = info_string[lastname_end+1:]
    firstname_end= info_string.find("\t")
    firstname = info_string[1:firstname_end]
    info_string = info_string[firstname_end:]
    return str.title(firstname)+" "+str.title(lastname), info_string

    
def parse_actor_data(actor_data):
    actor_dict={}
    movie_list=[]
    data_string = str(actor_data) #changes data into a workable string
    data_string = data_string[data_string.find("THE ACTORS LIST"):]
    info_string = data_string[data_string.find("	------")+8:data_string.find("---------------------------")+1]
#####above takes out the the unrequired information
    while info_string.find(",")!=-1:
        name, info_string = find_name(info_string)
        info_string, movie_list = create_movie_list(info_string)
        actor_dict[name]=movie_list
    return actor_dict

############Invert actor dictionary###################
def invert_actor_dict(actor_dict):
    actors=[]+actor_dict.keys() #list for actors
    movies_of_actor = [] #list to store movie that actors are in
    invert_actor_dict = {} #dict to contain movies with actors
    for actor in actors:
        movies = actor_dict[actor]
        for movie in movies:
            if movie in movies_of_actor:
                invert_actor_dict[movie].append(actor)
            else:
                movies_of_actor.append(movie)
                invert_actor_dict[movie]=[actor]
    return invert_actor_dict

#######TO find connection from one actor to another (this will list other actors related to the specific actor)#########
def find_connection(actor_name, actor_dict, movie_dict,No_use):
    actor_name=str.title(actor_name)
    if actor_name not in actor_dict:
        return -1
    actor_list=[actor_name]
    movie_list = actor_dict[actor_name]
    linked_actor = [actor_name] #to record actors that are already linked
    linked_movies = [] #to recrod movie list
    record = []
    temp=[]
    while movie_list!=[]:
        movie=movie_list.pop()
        linked_movies.append(movie)
        actors=[]+movie_dict[movie]
        for actor in actors:
            if actor in linked_actor:
                continue
            else:
                linked_actor.append(actor)
                nmovie_list=actor_dict[actor]
                record.append([[movie, actor]])
    result = -1
    while record!=[]:
        link=record.pop()
        for a in link:
            if a[1] == "Kevin Bacon":
                result= link
                break
            else:
                p2_movie_list=actor_dict[a[1]]
                for movie1 in p2_movie_list:
                    if movie1 in linked_movies:
                        continue
                    else:
                        linked_movies.append(movie1)
                        actors=[]+movie_dict[movie1]
                        for actor in actors:
                            if actor=="Kevin Bacon":
                                result= link+[[movie1, actor]]
                                break
                            if actor in linked_actor:
                                continue
                            else:
                                linked_actor.append(actor)
                                nmovie_list=actor_dict[actor]
                                temp= temp+[link+[[movie1, actor]]]
                        record=temp
                        temp=[]

    return result



if __name__=="__main__":
    
    filename="small_actor_data.txt"
    reader=open(filename,"r") #note: this open the files as read only
    reader = reader.read()
    actor_dict = parse_actor_data(reader)
    movie_dict = invert_actor_dict(actor_dict)
    n=0
    while n!="":
        name = raw_input("Please enter an actor (or blank to exit):")
        actor_name=str.title(name)
        if name == "":
            print ("Thank you for playing! The largest Bacon Number you found was "+str(n)+".")
            break
        result= find_connection(actor_name, actor_dict, movie_dict,"test")
        print result
        if result ==-1:
            print actor_name+" has a Bacon Number of Infinity."
        else:
            connect = len(result)
            print (actor_name+" has a Bacon Number of "+str(connect)+".")
            while result!=[]:
                display=result.pop(0)
                movie_name=display[0]
                if display[1]=="Kevin Bacon":
                    print (actor_name+" was in "+movie_name+" with Kevin Bacon.")
                else:
                    print (actor_name+" was in "+movie_name+" with "+display[1]+".")
                    actor_name=display[1]
            if connect >n:
                n=connect
            
###################NEED TO LOOP AND record number of connection##############
