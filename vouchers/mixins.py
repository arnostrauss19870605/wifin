from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
import re


class OrganisorAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organisor."""
    def dispatch(self, request, *args, **kwargs):
        #if not request.user.is_authenticated or not request.user.is_organisor:
        
        if not request.user.is_authenticated:
            
                return redirect("/clinix/login")
      

        return super().dispatch(request, *args, **kwargs)