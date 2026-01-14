from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from feed.forms import TicketForm, ReviewForm
from feed.models import Ticket, Review


@login_required
def feed_index(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()

    feed_posts = sorted(
        list(tickets) + list(reviews),
        key=lambda post: post.time_created,
        reverse=True
    )
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
def update_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        if ticket.user == request.user:
            ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
            if ticket_form.is_valid():
                ticket_form.save()
                messages.success(request, "Ticket correctement mis à jour.")
            else:
                messages.error(request, "La mise à jour du ticket a échoué. Veuillez réessayer.")
        else:
            messages.success(request, "Vous ne pouvez pas modifier ce ticket.")
        return redirect('feed:feed')
    else:
        ticket_form = TicketForm(instance=ticket)

    return render(request, 'feed/update_ticket.html', {'ticket_form': ticket_form, "ticket": ticket})

@login_required
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        if ticket.user == request.user:
            ticket.delete()
            messages.success(request, "Ticket correctement supprimé.")
        else:
            messages.success(request, "Vous ne pouvez pas supprimer ce ticket.")
        return redirect('feed:feed')

    return render(request, 'feed/delete_ticket.html', {'ticket': ticket})

@login_required
def create_review(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            user = request.user

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
def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    ticket = review.ticket
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Critique correctement supprimée.")
        return redirect('feed:feed')

    return render(request, 'feed/delete_review.html', {'review': review, 'ticket': ticket})
