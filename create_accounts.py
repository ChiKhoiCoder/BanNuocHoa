"""
Script to create admin and user accounts for the Perfume Shop
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfume_shop.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

def create_accounts():
    print("🔧 Creating user accounts...")
    
    # Create Admin Account
    print("\n1️⃣ Creating Admin account...")
    if User.objects.filter(username='admin').exists():
        print("   ⚠️  Admin account already exists, deleting old one...")
        User.objects.filter(username='admin').delete()
    
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@perfumeshop.com',
        password='admin123456',
        first_name='Admin',
        last_name='User'
    )
    
    # Create or update admin profile
    profile, created = UserProfile.objects.get_or_create(user=admin_user)
    profile.role = 'admin'
    profile.phone = '0123456789'
    profile.address = '123 Admin Street'
    profile.city = 'Hà Nội'
    profile.state = 'Hoàn Kiếm'
    profile.save()
    
    print("   ✅ Admin account created successfully!")
    print("      Username: admin")
    print("      Password: admin123456")
    
    # Create User Account 1
    print("\n2️⃣ Creating User1 account...")
    if User.objects.filter(username='user1').exists():
        print("   ⚠️  User1 account already exists, deleting old one...")
        User.objects.filter(username='user1').delete()
    
    user1 = User.objects.create_user(
        username='user1',
        email='user1@example.com',
        password='user123456',
        first_name='Nguyễn',
        last_name='Văn A'
    )
    
    profile1, created = UserProfile.objects.get_or_create(user=user1)
    profile1.role = 'user'
    profile1.phone = '0987654321'
    profile1.address = '456 User Street'
    profile1.city = 'Hà Nội'
    profile1.state = 'Cầu Giấy'
    profile1.save()
    
    print("   ✅ User1 account created successfully!")
    print("      Username: user1")
    print("      Password: user123456")
    
    # Create User Account 2
    print("\n3️⃣ Creating User2 account...")
    if User.objects.filter(username='user2').exists():
        print("   ⚠️  User2 account already exists, deleting old one...")
        User.objects.filter(username='user2').delete()
    
    user2 = User.objects.create_user(
        username='user2',
        email='user2@example.com',
        password='user123456',
        first_name='Trần',
        last_name='Thị B'
    )
    
    profile2, created = UserProfile.objects.get_or_create(user=user2)
    profile2.role = 'user'
    profile2.phone = '0912345678'
    profile2.address = '789 Customer Avenue'
    profile2.city = 'Hồ Chí Minh'
    profile2.state = 'Quận 1'
    profile2.save()
    
    print("   ✅ User2 account created successfully!")
    print("      Username: user2")
    print("      Password: user123456")
    
    print("\n" + "="*60)
    print("✅ ALL ACCOUNTS CREATED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 Account Summary:")
    print("\n🔐 ADMIN ACCOUNT:")
    print("   Username: admin")
    print("   Password: admin123456")
    print("   URL: http://127.0.0.1:8000/admin/")
    print("\n👤 USER ACCOUNT 1:")
    print("   Username: user1")
    print("   Password: user123456")
    print("\n👤 USER ACCOUNT 2:")
    print("   Username: user2")
    print("   Password: user123456")
    print("\n🌐 Login URL: http://127.0.0.1:8000/accounts/login/")
    print("="*60)

if __name__ == '__main__':
    create_accounts()
