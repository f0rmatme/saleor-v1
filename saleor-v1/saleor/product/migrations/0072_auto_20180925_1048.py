# Generated by Django 2.0.8 on 2018-09-25 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("product", "0071_attributechoicevalue_value")]

    operations = [
        migrations.RenameModel(old_name="ProductAttribute", new_name="Attribute"),
        migrations.RenameModel(
            old_name="AttributeChoiceValueTranslation",
            new_name="AttributeValueTranslation",
        ),
        migrations.RenameModel(
            old_name="AttributeChoiceValue", new_name="AttributeValue"
        ),
        migrations.RenameModel(
            old_name="ProductAttributeTranslation", new_name="AttributeTranslation"
        ),
        migrations.RenameField(
            model_name="attributetranslation",
            old_name="product_attribute",
            new_name="attribute",
        ),
        migrations.RenameField(
            model_name="attributevaluetranslation",
            old_name="attribute_choice_value",
            new_name="attribute_value",
        ),
        migrations.AlterUniqueTogether(
            name="attributetranslation",
            unique_together={("language_code", "attribute")},
        ),
        migrations.AlterUniqueTogether(
            name="attributevaluetranslation",
            unique_together={("language_code", "attribute_value")},
        ),
    ]
