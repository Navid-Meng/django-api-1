from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

# Serialization basically means that we are converting the python object
# into a json object so that we can send it to the client (frontend or mobile).

# Serialization is useful because:
# 1. The frontend or mobile app needs JSON, not Python objects
# 2. APIs communicate in JSON, not Python objects
# 3. We need to control which fields are exposed via our API
# 4. We want to validate incoming data before saving it to our database


class UserSerializer(serializers.ModelSerializer):
    '''
        Serializer for the User model.
        Converts User model instances to/from JSON format.
    '''
    class Meta:
        # Specify which model to serialize
        model = User
        
        # Define which fields to include in the serialization
        # Only id, username, and email will be visible in the API responses
        fields = ('id', 'username', 'email')
        
        # Specify fields that should be read-only
        # 'id' is read-only because it's automatically generated
        # and shouldn't be modifiable via API
        read_only_fields = ('id',)
        
        # Note: Any field not in 'fields' tuple will be excluded from serialization
        # even if it exists in the User model
        

class RegisterSerializer(serializers.ModelSerializer):
    '''
    Serializer for user registration.
    Handles creation of new user accounts with password validation.
    '''

    # Custom field for password with validation
    password = serializers.CharField(
        write_only=True, # Password will never be sent in API responses
        required=True, # Field is mandatory
        validators=[validate_password], # Uses Django's built-in password validation
    )
    
    # Confirmation password field
    password2 = serializers.CharField(
        write_only=True, # Also never sent in API responses
        required=True, # Field is mandatory
    )
    
    is_staff = serializers.BooleanField(default=False)
    
    class Meta:
        model = User # Specify the model to serialize
        
        # Specify fields that will be included in registration
        fields = ('email', 'username', 'password', 'password2', 'is_staff')
        
    def validate(self, attrs):
        '''
        Custom validation method to ensure passwords match.
        attrs: Dictionary containing all field values
        '''
        
        # Check if password and confirmation password match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        '''
        Creates a new user instance.
        validated_data: Dictionary containing all validated field values
        '''
        
        # Remove password2 confirmation field as it's not needed for user creation
        validated_data.pop('password2')
        
        
        is_staff = validated_data.pop('is_staff', False)
        
        # Create new user using create_user() method
        #' ** unpacks the dictionary as keyword arguments
        # e.g., username='user', email='user@example.com', password='pass123'
        user = User.objects.create_user(**validated_data, is_staff=is_staff)
        return user