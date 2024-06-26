import base64
import io

from django.db import transaction, IntegrityError
from django.core.files.images import ImageFile
from datetime import datetime

from PocketServiceApp.models import *


head_admin_role = Role.objects.filter(role_type='Главный администратор').last()
head_admin = Administrator.objects.filter(role=head_admin_role).last()


def exist_user_check_status(telegram_id, telegram_username):
    user = Person.objects.filter(telegram_id=str(telegram_id))
    if user.count() > 0:
        roles = user.last().role

        if roles.filter(role_type='Агент').last():
            return Agent.objects.filter(telegram_id=str(telegram_id))
        elif roles.filter(role_type='Клиент').last():
            return Client.objects.filter(telegram_id=str(telegram_id))
        else:
            return Administrator.objects.filter(telegram_id=str(telegram_id))
    else:
        user = Person.objects.filter(telegram_username=str(telegram_username))
        if user.count() > 0:
            roles = user.last().role

            if roles.filter(role_type='Агент').last():
                return Agent.objects.filter(telegram_username=str(telegram_username))
            elif roles.filter(role_type='Клиент').last():
                return Client.objects.filter(telegram_username=str(telegram_username))
            else:
                return Administrator.objects.filter(telegram_username=str(telegram_username))

    return False


def save_user(role_type=None, name=None, surname=None, patronymic=None, person_fio=None, date_of_birth=None,
              phone_number=None, telegram_chat_id=None, telegram_id=None, telegram_username=None, telegram_name=None,
              telegram_surname=None, email=None, background_image=None, address=None,addition_information=None):

    ### TODO: Расписать обновление специфичных полей для агента и админа (наподобие с try-except для полей клиента)
    ###       тоже самое и со созданием админов и агентов
    persons = exist_user_check_status(telegram_id, telegram_username)
    with transaction.atomic():
        print('USER START UPDATE')
        if persons and persons.count() > 0:
            person = persons.last()
            if telegram_id:
                person.telegram_id = telegram_id
            if name:
                person.name = name
            if surname:
                person.surname = surname
            if patronymic:
                person.patronymic = patronymic
            if person_fio:
                person.person_fio = person_fio
            if date_of_birth:
                person.date_of_birth = date_of_birth
            if phone_number:
                person.phone_number = phone_number
            if telegram_chat_id:
                person.telegram_chat_id = telegram_chat_id
            if telegram_username:
                person.telegram_username = telegram_username
            if telegram_name:
                person.telegram_name = telegram_name
            if telegram_surname:
                person.telegram_surname = telegram_surname
            if email:
                person.email = email
            if background_image:
                person.background_image = background_image
            try:
                if address:
                    person.address = address
            except AttributeError:
                pass
            try:
                if addition_information:
                    person.addition_information = addition_information
            except AttributeError:
                pass
            person.save()
            print('USER UPDATED')
            return True
        else:
            role = Role.objects.filter(role_type=str(role_type)).last()
            print('USER START CREATE')
            try:
                if "агент" in role_type:
                    new_user = Agent.objects.create(name=name, surname=surname, patronymic=patronymic,
                                                    date_of_birth=date_of_birth, phone_number=phone_number,
                                                    telegram_chat_id=telegram_chat_id,
                                                    telegram_id=telegram_id, telegram_username=telegram_username,
                                                    telegram_name=telegram_name, telegram_surname=telegram_surname,
                                                    email=email, background_image=background_image, address=address,
                                                    addition_information=addition_information)
                elif "администратор" in role_type:
                    new_user = Administrator.objects.create(name=name, surname=surname, patronymic=patronymic,
                                                            date_of_birth=date_of_birth, phone_number=phone_number,
                                                            telegram_chat_id=telegram_chat_id,
                                                            telegram_id=telegram_id, telegram_username=telegram_username,
                                                            telegram_name=telegram_name,
                                                            telegram_surname=telegram_surname, email=email,
                                                            background_image=background_image, address=address,
                                                            addition_information=addition_information)
                elif "Клиент" in role_type:
                    new_user = Client.objects.create(name=name, surname=surname, patronymic=patronymic,
                                                     date_of_birth=date_of_birth, phone_number=phone_number,
                                                     telegram_chat_id=telegram_chat_id,
                                                     telegram_id=telegram_id, telegram_username=telegram_username,
                                                     telegram_name=telegram_name, telegram_surname=telegram_surname,
                                                     email=email, background_image=background_image, address=address,
                                                     addition_information=addition_information)
                new_user.save()
                new_user.role.add(role)
                print('USER CREATED')
                return True
            except Exception as e:
                print(e)
                return False


def create_order(client_id, agent_id, product_id, order_name, order_price, order_start_time,
                 order_deadline, order_information):

    client = Client.objects.filter(telegram_id=str(client_id)).last()
    print(client)
    agent = Agent.objects.filter(telegram_id=str(agent_id)).last()
    print(agent)
    product = Product.objects.filter(id=product_id).last()
    print(product)
    print('order create start')

    with transaction.atomic():
        try:
            new_order = Order.objects.create(name=order_name, price=order_price, start_time=order_start_time,
                                             deadline=order_deadline, addition_information=order_information,
                                             client=client, agent=agent, product=product, administrator=head_admin)
            print("Order created")
            return new_order.id
        except Exception as e:
            print(e)
            return False


def update_order(order_id, reminder_status=None, control_flag=None):
    with transaction.atomic():
        orders = Order.objects.filter(id=str(order_id))
        if orders.count() > 0:
            if reminder_status is not None:
                orders.update(reminder_status=reminder_status)
            if control_flag is not None:
                orders.update(control_flag=control_flag)
            return True
        else:
            return False


def create_comment(comment_photos, agent_id, client_telegram_id, order_id, rating, comment_text):
    client = Client.objects.filter(telegram_id=str(client_telegram_id)).last()
    print(client)
    agent = Agent.objects.filter(id=str(agent_id)).last()
    print(agent)
    order = Order.objects.filter(id=order_id).last()
    print(order)
    print('comment create start')

    with transaction.atomic():
        try:
            new_comment = Comment.objects.create(client=client, agent=agent, order=order, rating=rating,
                                                 text=comment_text)
            print("Comment created")

            try:
                for photo in comment_photos:
                    image = ImageFile(io.BytesIO(base64.b64decode(photo[1].encode())), name=f'{photo[0]}.jpg')
                    CommentImages.objects.create(image_object=image, comment=new_comment)
                    print("Photo created")
            except Exception as e:
                print(e)

            return new_comment.id

        except Exception as e:
            print(e)
            return False


async def tg_message(bot, telegram_id, content, messages=None):
    try:
        await bot.send_message(chat_id=telegram_id, text=content, parse_mode='HTML')
        if messages:
            for msg in messages:
                await bot.delete_message(chat_id=telegram_id, message_id=msg)
    except Exception as e:
        print(e)


def update_education(education_id, university_name=None, specialization_name=None, education_end=None):
    with transaction.atomic():
        education = Education.objects.filter(id=str(education_id))
        if education.count() > 0:
            education = education.last()
            print('Education START UPDATE')

            if university_name:
                education.university.name = university_name
            if specialization_name:
                education.specialization.name = specialization_name
            if education_end:
                education.period_end = education_end

            education.specialization.save()
            education.university.save()
            education.save()

            print('Education UPDATED')
            return True
        else:
            return False


def create_education(university_name=None, university_town=None, university_country=None, university_description=None,
                     specialization_name=None, specialization_description=None, education_start=None,
                     education_end=None, agent_id=None):
    print('education create start')

    with transaction.atomic():
        agent = Agent.objects.filter(id=str(agent_id)).last()
        try:
            new_university = University.objects.create(name=university_name, town=university_town,
                                                       country=university_country, university_description=university_description)
            print("University created")
        except Exception as e:
            print("University not created", e)

        try:
            new_specialization = Specialization.objects.create(name=specialization_name,
                                                               specialization_description=specialization_description)
            print("specialization created")
        except Exception as e:
            print("specialization not created", e)

        try:
            new_education = Education.objects.create(university=new_university, specialization=new_specialization,
                                                     period_start=education_start, period_end=education_end,
                                                     document_check=False, agent=agent)
            print("education created")
            return new_education.id
        except Exception as e:
            print("education not created", e)
            return False


def update_price(price_id, price_value=None, product_info=None):
    with transaction.atomic():
        price = Price.objects.filter(id=str(price_id))
        if price.count() > 0:
            price = price.last()
            print('Price START UPDATE')

            if product_info:
                price.product.addition_information = product_info
            if price_value:
                price.price_value = price_value

            price.product.save()
            price.save()

            print('Price UPDATED')
            return True
        else:
            return False


def create_price(agent_id, price_value=None, product_info=None, product_type=None):
    print('price create start')

    with transaction.atomic():
        agent = Agent.objects.filter(id=str(agent_id)).last()
        try:
            new_product = Product.objects.create(product_type=product_type, addition_information=product_info)
            agent.products.add(new_product)
            print("Product created")
        except Exception as e:
            print("Product not created", e)

        try:
            new_price = Price.objects.create(price_value=price_value, product=new_product, agent=agent)
            print("price created")
            return new_price.id
        except Exception as e:
            print("price not created", e)
            return False
