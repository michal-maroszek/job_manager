import datetime
import folium
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from geopy.geocoders import Nominatim
from .models import Job, Client, User
from . import db
from sqlalchemy import and_


views = Blueprint("views", __name__)


def get_coords(address):
    """
    Function for "transforming" str address into a geographic latitude and longitude coordinates
    input: address -> str
    output: (latitude,longitude) -> (int, int)
    """
    if Job.location:
        geolocator = Nominatim(user_agent="job_manager")
        location = geolocator.geocode(address)
        if location == int:
            try:
                lat = location.latitude
                lon = location.longitude
                return lat, lon
            except (AttributeError, TypeError, ValueError):
                return (None, None)
        else:
            return (None, None)


@views.route("/")
def home():
    return render_template("home.html", user=current_user)


# ----------------------------------------------------------------
# Clients
# ----------------------------------------------------------------


@views.route("/clients", methods=["GET", "POST"])
@login_required  # doesn't allow this function unless a user is logged in
def clients():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        company = request.form.get("company")
        adress = request.form.get("adress")
        phone = request.form.get("phone")
        email = request.form.get("email")
        info = request.form.get("info")

        new_client = Client(
            user=current_user.id,
            firstname=firstname,
            lastname=lastname,
            company=company,
            adress=adress,
            phone=phone,
            email=email,
            info=info,
        )

        db.session.add(new_client)  # adding new client to database
        db.session.commit()  # committing db changes
        flash("Successfully added new client!", category="client_success")
        return redirect(url_for("views.clients"))

    return render_template("clients.html", user=current_user)


@views.route(f"/client<int:id>", methods=["GET", "POST"])
@login_required  # doesn't allow this function unless a user is logged in
def client_details(id):
    all_user_clients = Client.query.filter_by(user=current_user.id)
    current_client = all_user_clients.filter_by(id=id).first()
    if request.method == "POST":
        new_firstname = request.form.get("firstname")
        new_lastname = request.form.get("lastname")
        new_company = request.form.get("company")
        new_adress = request.form.get("adress")
        new_phone = request.form.get("phone")
        new_email = request.form.get("email")
        new_info = request.form.get("info")

        current_client.firstname = new_firstname
        current_client.lastname = new_lastname
        current_client.company = new_company
        current_client.adress = new_adress
        current_client.phone = new_phone
        current_client.email = new_email
        current_client.info = new_info

        db.session.commit()
        flash("Client data updated!", category="client_success")
        return redirect(url_for("views.clients"))

    return render_template(
        "client_details.html", user=current_user, current_client=current_client
    )


@views.route(f"/delete_client<int:id>", methods=["GET", "POST"])
@login_required  # doesn't allow this function unless a user is logged in
def delete_client(id):
    all_user_clients = Client.query.filter_by(user=current_user.id)
    current_client = all_user_clients.filter_by(id=id).first()
    db.session.delete(current_client)
    db.session.commit()
    flash("Client was successfully deleted!", category="client_success")
    return redirect(url_for("views.clients"))


# ----------------------------------------------------------------
# Jobs
# ----------------------------------------------------------------


# view for showing a list of all jobs and a form for adding new ones
@views.route("/jobs_list", methods=["GET", "POST"])
@login_required  # doesn't allow this function unless a user is logged in
def jobs_list():
    if request.method == "POST":
        name = request.form.get("name")
        job = Job.query.filter(
            and_(Job.name == name, Job.user == current_user.id)
        ).first()  # .first() return first occurance of given name of job if it exists,
        if job:
            flash("Job with this name already exists!", category="job_error")
        else:
            client = request.form.get("client")  # pass existing client
            location = request.form.get("location")
            job_type = request.form.get("job_type")
            status = request.form.get("status")
            start_time = request.form.get("start_time")
            end_time = request.form.get("end_time")
            info = request.form.get("info")
            coords_lat = get_coords(location)[0]
            # accessing the returned latitude from get_coords function
            coords_lon = get_coords(location)[1]
            # accessing the returned longitude from get_coords function

            new_job = Job(
                user=current_user.id,
                client=client,
                name=name,
                location=location,
                job_type=job_type,
                status=status,
                start_time=datetime.date.fromisoformat(str(start_time)),
                end_time=datetime.date.fromisoformat(str(end_time)),
                info=info,
                lat=coords_lat,
                lon=coords_lon,
            )
            db.session.add(new_job)  # adding new client to database
            db.session.commit()  # committing db changes
            flash("Successfully added new job!", category="job_success")
            return redirect(url_for("views.jobs_list"))

    return render_template("jobs_list.html", user=current_user)


# view for editing job data
@views.route("/job<int:id>", methods=["GET", "POST"])
@login_required  # doesn't allow this function unless a user is logged in
def current_job(id):
    current_user_jobs = Job.query.filter_by(user=current_user.id)
    current_job = current_user_jobs.filter_by(id=id).first()

    current_start_time = current_job.start_time.date().isoformat()
    current_end_time = current_job.end_time.date().isoformat()

    current_user_clients = Client.query.filter_by(user=current_user.id)
    current_job_client = current_user_clients.filter_by(id=current_job.client).first()

    if request.method == "POST":
        new_name = request.form.get("name")
        new_client = request.form.get("client")  # pass existing client
        new_location = request.form.get("location")
        new_job_type = request.form.get("job_type")
        new_status = request.form.get("status")
        new_start_time = request.form.get("start_time")
        new_end_time = request.form.get("end_time")
        new_info = request.form.get("info")
        new_coords_lat = get_coords(new_location)[0]
        # accessing the returned latitude from get_coords function
        new_coords_lon = get_coords(new_location)[1]
        # accessing the returned longitude from get_coords function

        current_job.client = new_client
        current_job.name = new_name
        current_job.location = new_location
        current_job.job_type = new_job_type
        current_job.status = new_status
        current_job.start_time = datetime.date.fromisoformat(str(new_start_time))
        current_job.end_time = datetime.date.fromisoformat(str(new_end_time))
        current_job.info = new_info
        current_job.lat = new_coords_lat
        current_job.lon = new_coords_lon

        db.session.commit()  # committing db changes
        flash("Successfully updated job data!", category="job_success")
        return redirect(url_for("views.jobs_list"))

    return render_template(
        "job_details.html",
        user=current_user,
        current_job=current_job,
        current_start_time=current_start_time,
        current_end_time=current_end_time,
        current_job_client=current_job_client,
    )


@views.route("/job/<filter>", methods=["GET", "POST"])
@login_required  # doesn't allow this function unless a user is logged in
def filter_jobs(filter):
    if filter == "name":
        jobs_name_order = Job.query.order_by(and_(Job.name), (Job.id))
        return render_template(
            "jobs_list_sorted.html", user=current_user, jobs_name_order=jobs_name_order
        )
    else:
        return redirect(url_for("views.jobs_list"))

    """
    jobs_type_order = None
    jobs_status_order = None
    jobs_endtime_order = None

    return redirect(url_for("views.jobs_list"))

    return render_template(
        "job_details.html",
        user=current_user,
        current_job=current_job,
        current_start_time=current_start_time,
        current_end_time=current_end_time,
        current_job_client=current_job_client,
    )
    """


# ----------------------------------------------------------------
# Jobs map
# ----------------------------------------------------------------


# view for rendering a map with all jobs markers shown
@views.route("/jobs_map", methods=["GET", "POST"])
@login_required  # doesn't allow this function unless a user is logged in
def jobs_map():
    all_jobs_coord = []
    all_jobs_lat = []
    all_jobs_lon = []

    if current_user.jobs:
        for job in current_user.jobs:
            # in case a job was given wrong adress and doesn't have valid coords
            if job.lat or job.lon == int:
                coords = (job.lat, job.lon)
                lat = job.lat
                lon = job.lon
                all_jobs_coord.append(coords)
                all_jobs_lat.append(lat)
                all_jobs_lon.append(lon)
            else:
                continue

        # calculating average coords to center the map based on all jobs markers
        avg_lat = sum(all_jobs_lat) / len(all_jobs_lat)
        avg_lon = sum(all_jobs_lon) / len(all_jobs_lon)
        average_coords = (avg_lat, avg_lon)

        map = folium.Map(location=average_coords, zoom_start=9, control_scale=True)

        # creating markes for each job based on their coords
        for job_marker in current_user.jobs:
            # in case a job was given wrong adress and doesn't have valid coords
            if job_marker.lat or job_marker.lon == int:
                folium.Marker(
                    location=[job_marker.lat, job_marker.lon],
                    tooltip=job_marker.name,
                    popup=f"{job_marker.name}\n{job_marker.job_type}\n{job_marker.status}\n{job_marker.end_time}\n{job_marker.info}",
                    icon=folium.Icon(color="red"),
                ).add_to(map)
            else:
                continue
    else:
        map = folium.Map(
            location=(51.9189046, 19.1343786), zoom_start=10, control_scale=True
        )

    return render_template("jobs_map.html", user=current_user, map=map._repr_html_())


# view for showing specific job marker on a map
@views.route("/jobs_map<int:id>", methods=["GET", "POST"])
@login_required  # doesn't allow this function unless a user is logged in
def current_job_map(id):
    current_user_jobs = Job.query.filter_by(user=current_user.id)
    current_job = current_user_jobs.filter_by(id=id).first()

    if current_job.lat or current_job.lon == int:
        coords = (current_job.lat, current_job.lon)
        lat = current_job.lat
        lon = current_job.lon

        map = folium.Map(location=coords, zoom_start=15, control_scale=True)

        folium.Marker(
            location=[lat, lon],
            tooltip=current_job.name,
            popup=f"{current_job.name}\n{current_job.job_type}\n{current_job.status}\n{current_job.end_time}\n{current_job.info}",
            icon=folium.Icon(color="red"),
        ).add_to(map)

        return render_template(
            "jobs_map.html", user=current_user, map=map._repr_html_()
        )

    else:
        flash(
            "Selected job doesn't have a valid coordinates. Check job adress.",
            category="job_error",
        )
        map = folium.Map(
            location=(51.9189046, 19.1343786), zoom_start=10, control_scale=True
        )

        return render_template(
            "jobs_map.html", user=current_user, map=map._repr_html_()
        )
