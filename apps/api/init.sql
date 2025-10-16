-- PostgreSQL初期化スクリプト
-- データベースとテーブルを作成

-- データベースが存在しない場合は作成（通常はdocker-composeで自動作成される）
-- CREATE DATABASE IF NOT EXISTS mokabu_lens;

-- 拡張機能を有効化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 基本的なテーブル構造はSQLAlchemyのマイグレーションで管理
-- ここでは初期データの挿入などを行う
