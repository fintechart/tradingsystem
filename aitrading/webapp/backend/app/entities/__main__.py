# coding=utf-8

def main():
  from .entity import engine, Base
  from .users import User 
  # if needed, generate database schema
  Base.metadata.create_all(engine)
  engine.dispose()

if __name__ == "__main__":
  main()
