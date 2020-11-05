from django.urls import reverse

from rate.models import ContactUs, Feedback


def test_index(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200


def test_contact_us_get_form(client):
    url = reverse('rate:contact-us-create')
    response = client.get(url)
    assert response.status_code == 200


def test_contact_us_post_form_empy_data(client):
    contact_us_initial_count = ContactUs.objects.count()
    url = reverse('rate:contact-us-create')
    response = client.post(url, data={})
    assert response.status_code == 200
    assert response.context_data['form'].errors == {
        'email': ['This field is required.'],
        'subject': ['This field is required.'],
        'text': ['This field is required.']}
    assert ContactUs.objects.count() == contact_us_initial_count


def test_contact_us_post_form_wrong_email(client):
    contact_us_initial_count = ContactUs.objects.count()
    url = reverse('rate:contact-us-create')
    data = {
        'email': 'this-is-wrong-email',
        'subject': 'Subject',
        'text': 'Text'
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context_data['form'].errors == {'email': ['Enter a valid email address.']}
    assert ContactUs.objects.count() == contact_us_initial_count


def test_contact_us_post_correct_data(client, fake):
    contact_us_initial_count = ContactUs.objects.count()
    url = reverse('rate:contact-us-create')
    data = {
        'email': 'this-is-correct-email@mail.com',
        'subject': fake.word(),
        'text': fake.word()
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert ContactUs.objects.count() == contact_us_initial_count + 1


def test_rate_list(client):
    response = client.get(reverse('rate:list'))
    assert response.status_code == 200


def test_rate_list_latest(client):
    response = client.get(reverse('rate:list-latest'))
    assert response.status_code == 200


def test_feedback_get_form(client):
    feedback_initial_count = Feedback.objects.count()
    response = client.get(reverse('rate:feedback'))
    assert response.status_code == 200
    assert Feedback.objects.count() == feedback_initial_count


def test_feedback_post_empty_data(client):
    feedback_initial_count = Feedback.objects.count()
    url = reverse('rate:feedback')
    response = client.post(url, data={})
    assert response.status_code == 200
    assert response.context_data['form'].errors == {'rating': ['This field is required.']}
    assert Feedback.objects.count() == feedback_initial_count


def test_feedback_post_data(client):
    feedback_initial_count = Feedback.objects.count()
    url = reverse('rate:feedback')
    data = {'rating': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert Feedback.objects.count() == feedback_initial_count + 1


def test_csv(client):
    url = reverse('rate:list-csv')
    response = client.get(url)
    assert response.status_code == 200


def test_xlsx(client):
    url = reverse('rate:list-xlsx')
    response = client.get(url)
    assert response.status_code == 200
