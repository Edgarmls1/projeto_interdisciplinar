create table dados_desmatamento(
	id serial primary key,
	data_registro date default current_date,
	estado varchar(50),
	area_desmatada_km2 float
);

create table recuperar(
	id_recuperar serial primary key,
	estado_recuperar varchar(50),
	num_arvores_plantar_m2 float
);

create or replace function calculo_reflorestamento()
returns trigger as $$
declare
	numero_arvores float;
begin
	numero_arvores := (new.area_desmatada_km2 * 1000) * 1/4;
	
	insert into recuperar values (default, new.estado, numero_arvores);
	
	return new;
end;
$$ language plpgsql;

create trigger calculo_reflorestamento
after insert on dados_desmatamento
for each row
execute function calculo_reflorestamento();

insert into dados_desmatamento values (default, now(), 'Pará', 2000.0)

select * from dados_desmatamento
