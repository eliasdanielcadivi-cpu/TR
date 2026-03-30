#!/usr/bin/gjs
const System = imports.system;
imports.gi.versions.Gtk = '3.0';
const {Gtk} = imports.gi;
Gtk.init(null);
// ARGB[] es el vector de parametros desde bash


let op = ARGV[0];

switch ( op ) {
	case "1": //Diálogo de dos botones con texto en Javascript
		function show_dialog(){
			let dialog = Gtk.Dialog.new();
			dialog.set_title(ARGV[1]);
			dialog.add_button(ARGV[2], Gtk.ResponseType.YES);
			dialog.add_button(ARGV[3], Gtk.ResponseType.NO);
			let box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 10);
			box.set_margin_top(10);
			box.set_margin_bottom(10);
			dialog.get_content_area().add(box);
			let label = Gtk.Label.new(ARGV[4]);
			box.pack_start(label, true, true, 5);
			let entry = Gtk.Entry.new();
			box.pack_start(entry, true, true, 5);
			dialog.show_all();
			try{
				let response = dialog.run();
				if(response === Gtk.ResponseType.YES && entry.get_text())
				{
					print(entry.get_text());
					return 1;
				}
				else if (response === Gtk.ResponseType.NO){
					
					return 2;
				}
				else{
				return 3
				}
				
				
				
				//print(entry.get_text());
			}
			catch(error){
				print(error);
				//return -1;
			}
			
			//return 0;
		}
		show_dialog();
	break;
	case "2":
		function show_dialog(){
			let dialog = Gtk.Dialog.new();
			dialog.set_title(ARGV[1]);
			dialog.add_button(ARGV[2], Gtk.ResponseType.YES);
			dialog.add_button(ARGV[3], Gtk.ResponseType.NO);
			let box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 10);
			box.set_margin_top(10);
			box.set_margin_bottom(10);
			dialog.get_content_area().add(box);
			let label = Gtk.Label.new(ARGV[4]);
			box.pack_start(label, true, true, 5);
			let entry = Gtk.Entry.new();
			box.pack_start(entry, true, true, 5);
			dialog.show_all();
			try{
				let response = dialog.run();
				if(response === Gtk.ResponseType.YES)
				{
					print(entry.get_text());
					return 1;
				}
				else if (response === Gtk.ResponseType.NO){
					
					return 2;
				}
				else{
				return 3
				}
				
				
				
				//print(entry.get_text());
			}
			catch(error){
				print(error);
				//return -1;
			}
			
			//return 0;
		}
		show_dialog();

		break;
	case "3":
		//
		break;
	default:
		print("Dialogo Javascript no encontrado")
		break;
}



