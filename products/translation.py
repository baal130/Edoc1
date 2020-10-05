from modeltranslation.translator import translator, TranslationOptions
from .models import Product,ProductRemark

class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
class ProductRemarkTranslationOptions(TranslationOptions):
    fields = ('descriptionremark',)

translator.register(Product, ProductTranslationOptions)
translator.register(ProductRemark, ProductRemarkTranslationOptions)