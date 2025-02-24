from api import app, db
from api.models import Usuario

def criar_admin():
    with app.app_context():
        # Verificar se o usuário já existe
        if not Usuario.query.filter_by(email='admin@admin.com').first():
            # Criar usuário admin
            admin = Usuario(
                nome='Administrador',
                email='admin@admin.com'
            )
            admin.set_senha('admin123')
            
            # Salvar no banco
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe!")

if __name__ == '__main__':
    criar_admin() 