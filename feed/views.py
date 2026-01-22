from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, AbstractUser
from django.core.paginator import Paginator

from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from django.shortcuts import render, redirect

from accounts.models import User
from feed.forms import TicketForm, ReviewForm, FollowUsersForm
from feed.models import Ticket, Review, UserFollows


@login_required
def feed_index(request: HttpRequest) -> HttpResponse:
    """
    View function for displaying the feed page with tickets and reviews from all the followed users.
    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        An HttpResponse with the feed page.
    """
    tickets = list(get_users_viewable_tickets(user=request.user).annotate(
        content_type=models.Value(value="Ticket", output_field=models.CharField())
    ))

    reviews = list(get_users_viewable_reviews(user=request.user).annotate(
        content_type=models.Value(value="Review", output_field=models.CharField())
    ))

    feed_posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    for post in feed_posts:
        if hasattr(post, "ticket"):
            ticket = post.ticket
        else:
            ticket = post

        ticket.user_has_reviewed = ticket.has_user_review(user=request.user)

    paginator = Paginator(object_list=feed_posts, per_page=5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(number=page_number)
    context = {'page_obj': page_obj}

    return render(request=request, template_name='feed/index.html', context=context)

@login_required
def posts(request: HttpRequest) -> HttpResponse:
    """
    View function for displaying the posts page of the current user with tickets and reviews.
    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        An HttpResponse with the posts page.
    """
    tickets = list(Ticket.objects.filter(user=request.user).annotate(
        content_type=models.Value(value="Ticket", output_field=models.CharField())
    ))

    reviews = list(Review.objects.filter(user=request.user).annotate(
        content_type=models.Value(value="Review", output_field=models.CharField())
    ))

    postspage_posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    paginator = Paginator(object_list=postspage_posts, per_page=5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(number=page_number)
    context = {'page_obj': page_obj}

    return render(request=request, template_name='feed/posts.html', context=context)

@login_required
def create_ticket(request: HttpRequest) -> HttpResponse:
    """
    View function for creating a new ticket.
    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        An HttpResponseRedirect to the feed page after ticket creation or
        An HttpResponse with the form of the ticket creation page.
    """
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            title = ticket_form.cleaned_data.get("title")
            description = ticket_form.cleaned_data.get("description")
            image = ticket_form.cleaned_data.get("image")
            user = request.user

            user.user_permissions.add(Permission.objects.get(codename='change_ticket'))
            user.user_permissions.add(Permission.objects.get(codename='delete_ticket'))

            Ticket.objects.create(
                title=title,
                description=description,
                user=user,
                image=image,
            )

            messages.success(request=request, message="✅ Ticket correctement publié.")
            return redirect(to='feed:feed')
        else:
            messages.error(request=request, message="❌ La publication du ticket a échoué. Veuillez réessayer.")
    else:
        ticket_form = TicketForm()

    return render(request=request, template_name='feed/create_ticket.html', context={'ticket_form': ticket_form})

@login_required
@permission_required(perm='feed.change_ticket', raise_exception=True)
def update_ticket(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    View function for updating an existing ticket.
    Args:
        request (HttpRequest): The incoming HTTP request.
        ticket_id (int): The ID of the ticket to update.

    Returns:
        An HttpResponseRedirect to the feed page afet ticket update or
        an HttpResponse with the update ticket form and its content to update.
    """
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            messages.success(request=request, message="✅ Ticket correctement mis à jour.")
        else:
            messages.error(request=request, message="❌ La mise à jour du ticket a échoué. Veuillez réessayer.")
        return redirect(to='feed:feed')
    else:
        ticket_form = TicketForm(instance=ticket)

    return render(request=request,
                  template_name='feed/update_ticket.html',
                  context={'ticket_form': ticket_form, "ticket": ticket})

@permission_required(perm='feed.delete_ticket', raise_exception=True)
@login_required
def delete_ticket(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    View function for deleting an existing ticket.
    Args:
        request (HttpRequest): The incoming HTTP request.
        ticket_id (int): The ID of the ticket to delete.

    Returns:
        An HttpResponseRedirect to the feed page afet ticket delete or
        An HttpResponse of the delete page with the ticket to delete.
    """
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request=request, message="✅ Ticket correctement supprimé.")
        return redirect(to='feed:feed')

    return render(request=request, template_name='feed/delete_ticket.html', context={'ticket': ticket})

@login_required
def create_review(request: HttpRequest) -> HttpResponse:
    """
    View function for creating a new review.
    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        An HttpResponseRedirect to the feed page after review creation or
        An HttpResponse to the creation page with the forms for the new review and its ticket.
    """
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            user = request.user

            user.user_permissions.add(Permission.objects.get(codename='change_review'))
            user.user_permissions.add(Permission.objects.get(codename='delete_review'))

            ticket = Ticket.objects.create(
                title=ticket_form.cleaned_data["title"],
                description=ticket_form.cleaned_data["description"],
                image=ticket_form.cleaned_data.get("image"),
                user=user,
            )

            Review.objects.create(
                ticket=ticket,
                headline=review_form.cleaned_data["headline"],
                rating=review_form.cleaned_data["rating"],
                body=review_form.cleaned_data["body"],
                user=user,
            )
            messages.success(request=request, message="✅ Critique correctement publiée.")
            return redirect(tp='feed:feed')
        else:
            messages.error(request=request, message="❌ La publication de la critique a échoué. Veuillez réessayer.")
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request=request,
                  template_name='feed/create_review.html',
                  context={'ticket_form': ticket_form, 'review_form': review_form})

@login_required
def create_review_by_answer(request: HttpRequest, ticket_id: int) -> HttpResponse:
    """
    View function for creating a new review by answer a ticket.
    Args:
        request (HttpRequest): The incoming HTTP request.
        ticket_id (int): The ID of the ticket to delete.

    Returns:
        An HttpResponseRedirect to the feed page after review creation or
        An HttpResponse to the creation by answer page with the forms of the new review and its ticket.
    """
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            user = request.user

            user.user_permissions.add(Permission.objects.get(codename='change_review'))
            user.user_permissions.add(Permission.objects.get(codename='delete_review'))

            Review.objects.create(
                ticket=ticket,
                headline=review_form.cleaned_data["headline"],
                rating=review_form.cleaned_data["rating"],
                body=review_form.cleaned_data["body"],
                user=user,
            )
            messages.success(request=request, message="✅ Critique correctement publiée.")
            return redirect(to='feed:feed')
        else:
            messages.error(request=request, message="❌ La publication de la critique a échoué. Veuillez réessayer.")
    else:
        review_form = ReviewForm()

    return render(request=request,
                  template_name='feed/create_review_by_answer.html',
                  context={'ticket': ticket, 'review_form': review_form})

@login_required
@permission_required(perm='feed.change_review', raise_exception=True)
def update_review(request, review_id):
    """
    View function for updating an existing review.
    Args:
        request (HttpRequest): The incoming HTTP request.
        review_id (int): The ID of the review to update.

    Returns:
        An HttpResponseRedirect to the feed page after review update or
        An HttpResponse to the review update page with the form of the review to update and its content.
    """
    review = Review.objects.get(id=review_id)
    ticket = review.ticket

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            messages.success(request, "✅ Critique correctement mise à jour.")
            return redirect('feed:feed')
        else:
            messages.error(request, "❌ La mise à jour de la critique a échoué. Veuillez réessayer.")
    else:
        review_form = ReviewForm(instance=review)

    return render(request=request,
                  template_name='feed/update_review.html',
                  context={'review_form': review_form, "ticket": ticket, "review": review})

@login_required
@permission_required(perm='feed.delete_review', raise_exception=True)
def delete_review(request: HttpRequest, review_id: int) -> HttpResponse:
    """
    View function for deleting an existing review.
    Args:
        request (HttpRequest): The incoming HTTP request.
        review_id (int): The ID of the review to delete.

    Returns:
        An HttpResponseRedirect to the feed page after review delete or
        An HttpResponse to the delete confirmation page with the review to delete.
    """
    review = Review.objects.get(id=review_id)
    ticket = review.ticket
    if request.method == 'POST':
        review.delete()
        messages.success(request=request, message="✅ Critique correctement supprimée.")
        return redirect(to='feed:feed')

    return render(request=request,
                  template_name='feed/delete_review.html',
                  context={'review': review, 'ticket': ticket})

@login_required
def follow_user(request: HttpRequest) -> HttpResponse:
    """
    View function for displaying followed people and followers.
    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        An HttpResponseRedirect to the subscribers page after adding people to follow or
        An HttpResponse of the follow page with the form to add people and all the followed people and followers.
    """
    if request.method == "POST":
        follow_form = FollowUsersForm(request.POST, user=request.user)
        if follow_form.is_valid():
            UserFollows.objects.create(user=request.user, followed_user=follow_form.followed_user)
            messages.success(request=request, message=f"✅ Abonnement à \"{follow_form.followed_user}\" réussi.")
        else:
            for error in follow_form.errors.values():
                messages.error(request=request, message=str(error))

        return redirect(to="feed:follows")
    else:
        follow_form = FollowUsersForm(user=request.user)

    following = (UserFollows.objects.filter(user=request.user).select_related("followed_user"))

    followed_by = (UserFollows.objects.filter(followed_user=request.user).select_related("user"))

    return render(request=request,
                  template_name="feed/followers.html",
                  context={"follow_form": follow_form, "following": following, "followed_by": followed_by,})

def delete_follow_user(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    View function for deleting followed users.
    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (int): The ID of the user to delete.

    Returns:
        An HttpResponseRedirect to the subscribers page after deletion of the user or
        An HttpResponse of the delete confirmation page with the username of the followed user to delete.
    """
    followed_user = User.objects.get(id=user_id)
    if request.method == "POST":
        userFollow = UserFollows.objects.get(user=request.user, followed_user=followed_user)
        userFollow.delete()
        messages.success(request=request,
                         message=f"✅ L'utilisateur \"{followed_user.username}\" correctement supprimé.")
        return redirect(to='feed:follows')

    return render(request=request,
                  template_name='feed/delete_followed_user.html',
                  context={'username': followed_user.username})


def get_users_viewable_tickets(user: AbstractUser) -> QuerySet[Ticket]:
    """
    Method for getting user viewable tickets.
    Args:
        user (AbstractUser): The user to get viewable tickets for.

    Returns:
        A QuerySet with the viewable tickets.
    """
    followed_users = UserFollows.objects.filter(user=user).values_list(
        "followed_user", flat=True
    )

    return Ticket.objects.filter(user__in=followed_users)



def get_users_viewable_reviews(user: AbstractUser) -> QuerySet[Review]:
    """
    Method for getting user viewable reviews.
    Args:
        user (AbstractUser): The user to get viewable reviews for.

    Returns:
        A QuerySet with the viewable reviews.
    """
    followed_users = UserFollows.objects.filter(user=user).values_list(
        "followed_user", flat=True
    )

    return Review.objects.filter(user__in=followed_users)
