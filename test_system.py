from system_architecture import UserRole, SystemState, NavigationMenu, UserProfile

print('=== System Architecture Test ===\n')

# Test UserProfile
profile = UserProfile('test_user', UserRole.TENANT)
print(f'✓ Created UserProfile: {profile.user_id}, role={profile.role}')

# Test SystemState  
state = SystemState()
print(f'✓ SystemState initialized')

# Test Navigation for different roles
print('\nNavigation Menus:')
for role in [UserRole.TENANT, UserRole.ADVOCATE, UserRole.ADMIN]:
    menu = NavigationMenu.get_menu_for_role(role)
    print(f'\n{role.upper()} menu ({len(menu)} items):')
    for item in menu:
        print(f'  - {item["label"]}: {item["url"]}')

print('\n✓ All system architecture components working!')
