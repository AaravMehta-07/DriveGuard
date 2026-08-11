import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class LocalDatabase {
  static final LocalDatabase instance = LocalDatabase._init();
  static Database? _database;

  LocalDatabase._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('driveguard.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(path, version: 1, onCreate: _createDB);
  }

  Future _createDB(Database db, int version) async {
    const idType = 'INTEGER PRIMARY KEY AUTOINCREMENT';
    const textType = 'TEXT NOT NULL';
    const realType = 'REAL NOT NULL';
    const integerType = 'INTEGER NOT NULL';

    await db.execute('''
CREATE TABLE compliance_packs (
  id $idType,
  name $textType,
  version $textType,
  data $textType
)
''');

    await db.execute('''
CREATE TABLE places (
  id $idType,
  name $textType,
  latitude $realType,
  longitude $realType,
  address $textType
)
''');
  }

  Future<void> insertPlace(Map<String, dynamic> place) async {
    final db = await instance.database;
    await db.insert('places', place);
  }

  Future<List<Map<String, dynamic>>> fetchPlaces() async {
    final db = await instance.database;
    return await db.query('places');
  }

  Future<void> close() async {
    final db = await instance.database;
    db.close();
  }
}
