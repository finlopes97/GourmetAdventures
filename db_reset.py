#Database initialization (can be deleted at the end)
from website import db, create_app
app=create_app()
ctx=app.app_context()
ctx.push()
db.create_all()
quit()