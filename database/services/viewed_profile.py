from database.services.base import BaseService
from ..models.viewed_profile import ViewedProfileModel


class ViewedProfile(BaseService):
    model = ViewedProfileModel