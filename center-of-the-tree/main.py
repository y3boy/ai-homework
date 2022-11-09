from vk_api import VkApi
from vk_api.vk_api import VkApiMethod
import networkx as nx
import matplotlib.pyplot as plt

def auth_handler():
    # Code of two step auth
    key = input("Enter authentication code: ")
    
    remember_device = False

    return key, remember_device


def authorization():
    with open('.env') as file:
        lines = file.readlines()
    
    vk_session = VkApi(
        login=lines[0],
        password=lines[1],
        auth_handler=auth_handler
    )
    vk_session.auth()

    return vk_session.get_api()


def create_friends_of_friends_tree(vk_client: VkApiMethod):
    used_id = dict()
    current_user_id = vk_client.users.get()[0].get('id')
    # print(vk_client.friends.getLists(2004762))
    used_id[current_user_id] = 1

    G = nx.Graph()
    G.add_node(current_user_id)
    
    for friend_id in vk_client.friends.get().get('items'):
        G.add_node(friend_id)
        G.add_edge(current_user_id, friend_id)
        
        for friend_of_friends_id in vk_client.friends.get(friend_id).get('items'):
            if used_id.get(friend_of_friends_id) is None:
                G.add_node(friend_of_friends_id)
                used_id[friend_of_friends_id] = 1
            G.add_edge(friend_id, friend_of_friends_id)


    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


def main():
    client = authorization()
    create_friends_of_friends_tree(vk_client=client)


if __name__ == '__main__':
    main()