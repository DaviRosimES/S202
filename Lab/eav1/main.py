from DAO.motoristaDAO import MotoristaDAO
from DAO.passageiroDAO import PassageiroDAO
from DAO.corridaDAO import CorridaDAO
from CLI.motoristaCLI import MotoristaCLI
from database.database import Database

db = Database(database="eav1", collection="Motoristas")

motorista_dao = MotoristaDAO(db)
passageiro_dao = PassageiroDAO(db)
corrida_dao = CorridaDAO(db)

motorista_cli = MotoristaCLI(motorista_dao, passageiro_dao, corrida_dao)
motorista_cli.run()
