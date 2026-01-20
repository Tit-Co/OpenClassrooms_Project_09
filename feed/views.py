from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission

from django.db import models

from django.shortcuts import render, redirect

from feed.forms import TicketForm, ReviewForm, FollowUsersForm
from feed.models import Ticket, Review, UserFollows


@login_required
def feed_index(request):
    tickets = list(get_users_viewable_tickets(request.user).annotate(
        content_type=models.Value("Ticket", output_field=models.CharField())
    ))

    reviews = list(get_users_viewable_reviews(request.user).annotate(
        content_type=models.Value("Review", output_field=models.CharField())
    ))

    reviewed_ticket_ids = set(
        Review.objects.filter(user=request.user)
        .values_list("ticket_id", flat=True)
    )

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

        ticket.user_has_reviewed = ticket.has_user_review(request.user)

    return render(request, 'feed/index.html', context={'feed_posts': feed_posts})

@login_required
def create_ticket(request):
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

            messages.success(request, "Ticket correctement publié.")
            return redirect('feed:feed')
        else:
            messages.error(request, "La publication du ticket a échoué. Veuillez réessayer.")
    else:
        ticket_form = TicketForm()

    return render(request, 'feed/create_ticket.html', {'ticket_form': ticket_form})

@login_required
@permission_required('feed.change_ticket', raise_exception=True)
def update_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            messages.success(request, "Ticket correctement mis à jour.")
        else:
            messages.error(request, "La mise à jour du ticket a échoué. Veuillez réessayer.")
        return redirect('feed:feed')
    else:
        ticket_form = TicketForm(instance=ticket)

    return render(request, 'feed/update_ticket.html', {'ticket_form': ticket_form, "ticket": ticket})

@permission_required('feed.delete_ticket', raise_exception=True)
@login_required
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Ticket correctement supprimé.")
        return redirect('feed:feed')

    return render(request, 'feed/delete_ticket.html', {'ticket': ticket})

@login_required
def create_review(request):
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
            messages.success(request, "Critique correctement publiée.")
            return redirect('feed:feed')
        else:
            messages.error(request, "La publication de la critique a échoué. Veuillez réessayer.")
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, 'feed/create_review.html', {'ticket_form': ticket_form, 'review_form': review_form})

@login_required
def create_review_by_answer(request, ticket_id):
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
            messages.success(request, "Critique correctement publiée.")
            return redirect('feed:feed')
        else:
            messages.error(request, "La publication de la critique a échoué. Veuillez réessayer.")
    else:
        review_form = ReviewForm()

    return render(request, 'feed/create_review_by_answer.html', {'ticket': ticket, 'review_form': review_form})

@login_required
@permission_required('feed.change_review', raise_exception=True)
def update_review(request, review_id):
    review = Review.objects.get(id=review_id)
    ticket = review.ticket

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            messages.success(request, "Critique correctement mise à jour.")
            return redirect('feed:feed')
        else:
            messages.error(request, "La mise à jour de la critique a échoué. Veuillez réessayer.")
    else:
        review_form = ReviewForm(instance=review)

    return render(request, 'feed/update_review.html', {'review_form': review_form, "ticket": ticket, "review": review})

@login_required
@permission_required('feed.delete_review', raise_exception=True)
def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    ticket = review.ticket
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Critique correctement supprimée.")
        return redirect('feed:feed')

    return render(request, 'feed/delete_review.html', {'review': review, 'ticket': ticket})

@login_required
def follow_user(request):
    if request.method == "POST":
        follow_form = FollowUsersForm(request.POST, user=request.user)
        if follow_form.is_valid():
            UserFollows.objects.create(user=request.user, followed_user=follow_form.followed_user)
            messages.success(request, "Abonnement réussi.")
        else:
            for error in follow_form.errors.values():
                messages.error(request, str(error))

        return redirect("feed:follows")
    else:
        follow_form = FollowUsersForm(user=request.user)

    following = (UserFollows.objects.filter(user=request.user).select_related("followed_user"))

    followed_by = (UserFollows.objects.filter(followed_user=request.user).select_related("user"))

    return render(request,"feed/followers.html",
                  {"follow_form": follow_form, "following": following, "followed_by": followed_by,})

def get_users_viewable_tickets(user):
    followed_users = UserFollows.objects.filter(user=user).values_list(
        "followed_user", flat=True
    )

    return Ticket.objects.filter(user__in=followed_users)



def get_users_viewable_reviews(user):
    followed_users = UserFollows.objects.filter(user=user).values_list(
        "followed_user", flat=True
    )

    return Review.objects.filter(user__in=followed_users)