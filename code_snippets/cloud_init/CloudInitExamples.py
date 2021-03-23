from code_snippets.cloud_init.models import MetaDataGenerator, VendorDataGenerator

mdg = MetaDataGenerator()
mdg.print_meta_data()

mdg2 = MetaDataGenerator('d0251e2c-66ae-4c6f-b8fa-f65418070ee6')
mdg2.print_meta_data()

vdg = VendorDataGenerator('test', 'test')
vdg.print_vendor_data()

vdg2 = VendorDataGenerator('test', 'test', False, False, False)
vdg2.print_vendor_data()
