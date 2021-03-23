from code_snippets.cloud_init.models import MetaDataGenerator, VendorDataGenerator

mdg = MetaDataGenerator()
mdg.render()

mdg2 = MetaDataGenerator('d0251e2c-66ae-4c6f-b8fa-f65418070ee6')
mdg2.render()

vdg = VendorDataGenerator('test', 'test')
vdg.render()

vdg2 = VendorDataGenerator('test', 'test', False, False, False)
vdg2.render()
