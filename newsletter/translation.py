from modeltranslation.translator import translator, TranslationOptions
from .models import UserDetails,UserDetailsService,UserDetailsTeam,UserDetailsServicePackagePrice 

class UserDetailsTranslationOptions(TranslationOptions):
    fields = ('about',)
class UserDetailsServiceTranslationOptions(TranslationOptions):
    fields = ('servicetext','servicename',)
class UserDetailsTeamTranslationOptions(TranslationOptions):
    fields = ('teamtext',)

class UserDetailsServicePackagePriceTranslationOptions(TranslationOptions):
    fields = ('headdescription','description','extragift',)
translator.register(UserDetails, UserDetailsTranslationOptions)
translator.register(UserDetailsService, UserDetailsServiceTranslationOptions)
translator.register(UserDetailsTeam, UserDetailsTeamTranslationOptions)
translator.register(UserDetailsServicePackagePrice, UserDetailsServicePackagePriceTranslationOptions)
