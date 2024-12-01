from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    phone_number = PhoneNumberField()
    activated_invite_code = serializers.SerializerMethodField()
    refs = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'invite_code', 'activated_invite_code', 'refs')

    def get_refs(self, obj):
        refs = obj.referals.all()
        return [str(ref.phone_number) for ref in refs]

    def get_activated_invite_code(self, obj):
        if obj.activated_invite_code:
            return obj.activated_invite_code.invite_code
        return None


class OTPSerializer(serializers.Serializer):

    phone_number = PhoneNumberField()
    otp = serializers.CharField(read_only=True)


class AuthSerializer(serializers.Serializer):

    otp = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        fields = ('phone_number', 'otp', 'token')


class ReferalSerializer(serializers.ModelSerializer):

    phone_number = PhoneNumberField()
    activated_invite_code = serializers.CharField(
        required=True,
        write_only=True
    )
    you_invited_by = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'activated_invite_code', 'you_invited_by')
        read_only_fields = ('phone_number', )

    def get_you_invited_by(self, obj):
        if obj.activated_invite_code:
            return obj.activated_invite_code.__str__()
        return None

    def update(self, instance, validated_data):
        activated_invite_code = validated_data.get('activated_invite_code', None)

        if activated_invite_code:
            try:
                user = User.objects.get(invite_code=activated_invite_code)
            except User.DoesNotExist:
                raise ValidationError('Your referal code is wrong!')

            if instance.activated_invite_code is None:
                instance.activated_invite_code = user
                instance.save()
                return instance
            else:
                raise ValidationError('Your referal code already exists!')
        return instance
