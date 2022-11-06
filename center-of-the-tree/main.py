from distutils.command.clean import clean
from vk_api import VkApi
from vk_api.vk_api import VkApiMethod
import networkx as nx


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
    print(vk_client.friends.get())
    print(vk_client.users.get(user_ids=151671305))


def main():
    client = authorization()
    create_friends_of_friends_tree(vk_client=client)


if __name__ == '__main__':
    main()
    
    