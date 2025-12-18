# Settings/views.py
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import (
    FunctionForm,
    PermissionGroupForm,
    ResponsibilityForm,
    RoleForm,
    ServiceForm,
    TypeOfServiceForm,
)
from .models import (
    Function,
    PermissionGroup,
    Responsibility,
    Role,
    Service,
    TypeOfService,
)


def _render_detail(request, obj, title, back_url, attributes):
    return render(
        request,
        "settings/detail.html",
        {
            "object": obj,
            "title": title,
            "back_url": back_url,
            "attributes": attributes,
        },
    )


# --- LIST VIEWS ---
def functions_list(request):
    functions = Function.objects.all()
    return render(
        request,
        'settings/functions_list.html',
        {
            'functions': functions,
            'function_form': FunctionForm(),
        },
    )

def types_of_service_list(request):
    types = TypeOfService.objects.all()
    return render(
        request,
        'settings/types_of_service_list.html',
        {
            'types': types,
            'type_form': TypeOfServiceForm(),
        },
    )

def services_list(request):
    services = Service.objects.select_related("type_of_service", "parent_service")
    available_levels = list(
        Service.objects.order_by("level").values_list("level", flat=True).distinct()
    )
    selected_level = request.GET.get("level")
    if selected_level:
        try:
            level_int = int(selected_level)
            services = services.filter(level=level_int)
        except ValueError:
            selected_level = None

    return render(
        request,
        'settings/services_list.html',
        {
            'services': services,
            'available_levels': available_levels,
            'selected_level': selected_level,
            'service_form': ServiceForm(),
        },
    )

def responsibilities_list(request):
    responsibilities = Responsibility.objects.all()
    return render(
        request,
        'settings/responsibilities_list.html',
        {
            'responsibilities': responsibilities,
            'responsibility_form': ResponsibilityForm(),
        },
    )


def permission_groups_list(request):
    groups = PermissionGroup.objects.prefetch_related("permissions")
    for group in groups:
        group.permission_ids = [str(pk) for pk in group.permissions.values_list("id", flat=True)]
    return render(
        request,
        "settings/permission_groups_list.html",
        {
            "groups": groups,
            "permission_group_form": PermissionGroupForm(),
        },
    )


def roles_list(request):
    roles = Role.objects.prefetch_related("permission_groups", "permissions")
    for role in roles:
        role.permission_group_ids = [str(pk) for pk in role.permission_groups.values_list("id", flat=True)]
        role.permission_ids = [str(pk) for pk in role.permissions.values_list("id", flat=True)]
    return render(
        request,
        "settings/roles_list.html",
        {
            "roles": roles,
            "role_form": RoleForm(),
        },
    )

# --- CREATE VIEWS ---
@require_POST
def create_function(request):
    form = FunctionForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Function created successfully.")
    else:
        messages.error(request, "Failed to create function. Please try again.")
    return redirect("functions_list")

@require_POST
def create_type_of_service(request):
    form = TypeOfServiceForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Type of service created successfully.")
    else:
        messages.error(request, "Failed to create type of service.")
    return redirect("types_of_service_list")

@require_POST
def create_service(request):
    form = ServiceForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Service created successfully.")
    else:
        messages.error(request, "Failed to create service. Please fix the errors and try again.")
    return redirect("services_list")

@require_POST
def create_responsibility(request):
    form = ResponsibilityForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Responsibility created successfully.")
    else:
        messages.error(request, "Failed to create responsibility.")
    return redirect("responsibilities_list")


@require_POST
def create_permission_group(request):
    form = PermissionGroupForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Permission group created successfully.")
    else:
        messages.error(request, "Failed to create permission group.")
    return redirect("permission_groups_list")


@require_POST
def create_role(request):
    form = RoleForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Role created successfully.")
    else:
        messages.error(request, "Failed to create role.")
    return redirect("roles_list")

# --- EDIT VIEWS ---
@require_POST
def edit_function(request, pk):
    function = get_object_or_404(Function, pk=pk)
    form = FunctionForm(request.POST, instance=function)
    if form.is_valid():
        form.save()
        messages.success(request, "Function updated successfully.")
    else:
        messages.error(request, "Failed to update function. Please try again.")
    return redirect("functions_list")

@require_POST
def edit_type_of_service(request, pk):
    type_obj = get_object_or_404(TypeOfService, pk=pk)
    form = TypeOfServiceForm(request.POST, instance=type_obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Type of service updated successfully.")
    else:
        messages.error(request, "Failed to update type of service.")
    return redirect("types_of_service_list")

@require_POST
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST, instance=service)
    if form.is_valid():
        form.save()
        messages.success(request, "Service updated successfully.")
    else:
        messages.error(request, "Failed to update service. Please fix the errors and try again.")
    return redirect("services_list")

@require_POST
def edit_responsibility(request, pk):
    responsibility = get_object_or_404(Responsibility, pk=pk)
    form = ResponsibilityForm(request.POST, instance=responsibility)
    if form.is_valid():
        form.save()
        messages.success(request, "Responsibility updated successfully.")
    else:
        messages.error(request, "Failed to update responsibility.")
    return redirect("responsibilities_list")


@require_POST
def edit_permission_group(request, pk):
    group = get_object_or_404(PermissionGroup, pk=pk)
    form = PermissionGroupForm(request.POST, instance=group)
    if form.is_valid():
        form.save()
        messages.success(request, "Permission group updated successfully.")
    else:
        messages.error(request, "Failed to update permission group.")
    return redirect("permission_groups_list")


@require_POST
def edit_role(request, pk):
    role = get_object_or_404(Role, pk=pk)
    form = RoleForm(request.POST, instance=role)
    if form.is_valid():
        form.save()
        messages.success(request, "Role updated successfully.")
    else:
        messages.error(request, "Failed to update role.")
    return redirect("roles_list")


# --- DELETE VIEWS ---
@require_POST
def delete_function(request, pk):
    function = get_object_or_404(Function, pk=pk)
    function.delete()
    messages.success(request, "Function deleted.")
    return redirect("functions_list")


@require_POST
def delete_type_of_service(request, pk):
    type_obj = get_object_or_404(TypeOfService, pk=pk)
    type_obj.delete()
    messages.success(request, "Type of service deleted.")
    return redirect("types_of_service_list")


@require_POST
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    messages.success(request, "Service deleted.")
    return redirect("services_list")


@require_POST
def delete_responsibility(request, pk):
    responsibility = get_object_or_404(Responsibility, pk=pk)
    responsibility.delete()
    messages.success(request, "Responsibility deleted.")
    return redirect("responsibilities_list")


@require_POST
def delete_permission_group(request, pk):
    group = get_object_or_404(PermissionGroup, pk=pk)
    group.delete()
    messages.success(request, "Permission group deleted.")
    return redirect("permission_groups_list")


@require_POST
def delete_role(request, pk):
    role = get_object_or_404(Role, pk=pk)
    role.delete()
    messages.success(request, "Role deleted.")
    return redirect("roles_list")


# --- DETAIL VIEWS ---
def function_detail(request, pk):
    function = get_object_or_404(Function, pk=pk)
    return _render_detail(
        request,
        function,
        "Function Details",
        reverse("functions_list"),
        [("UUID", function.id), ("Name", function.name)],
    )


def type_of_service_detail(request, pk):
    type_obj = get_object_or_404(TypeOfService, pk=pk)
    return _render_detail(
        request,
        type_obj,
        "Type of Service Details",
        reverse("types_of_service_list"),
        [("UUID", type_obj.id), ("Name", type_obj.name)],
    )


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return _render_detail(
        request,
        service,
        "Service Details",
        reverse("services_list"),
        [
            ("UUID", service.id),
            ("Name", service.name),
            ("Type", service.type_of_service.name if service.type_of_service else "—"),
            ("Level", service.level),
            ("Parent Service", service.parent_service or "—"),
        ],
    )


def responsibility_detail(request, pk):
    responsibility = get_object_or_404(Responsibility, pk=pk)
    return _render_detail(
        request,
        responsibility,
        "Responsibility Details",
        reverse("responsibilities_list"),
        [("UUID", responsibility.id), ("Name", responsibility.name)],
    )


def permission_group_detail(request, pk):
    group = get_object_or_404(PermissionGroup, pk=pk)
    permissions = ", ".join(group.permissions.values_list("codename", flat=True)) or "—"
    return _render_detail(
        request,
        group,
        "Permission Group Details",
        reverse("permission_groups_list"),
        [
            ("UUID", group.id),
            ("Name", group.name),
            ("Description", group.description or "—"),
            ("Permissions", permissions),
        ],
    )


def role_detail(request, pk):
    role = get_object_or_404(Role, pk=pk)
    groups = ", ".join(role.permission_groups.values_list("name", flat=True)) or "—"
    permissions = ", ".join(role.permissions.values_list("codename", flat=True)) or "—"
    return _render_detail(
        request,
        role,
        "Role Details",
        reverse("roles_list"),
        [
            ("UUID", role.id),
            ("Name", role.name),
            ("Description", role.description or "—"),
            ("Active", "Yes" if role.is_active else "No"),
            ("Permission Groups", groups),
            ("Direct Permissions", permissions),
        ],
    )
