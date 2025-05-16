package com.example.detecting_humans_in_sar;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    EditText name;
    Button submit;

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        name=findViewById(R.id.editTextTextPersonName6);
        submit=findViewById(R.id.button4);
        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String ip=name.getText().toString();
                int flag=0;
                if(ip.equalsIgnoreCase("")){
                    name.setError("Required");
                    flag++;
//                    Toast.makeText(MainActivity.this, "", Toast.LENGTH_SHORT).show();
                }
                if(flag==0) {
                    String url = "http://" + ip + ":5000";
                    SharedPreferences sh = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
                    SharedPreferences.Editor ed = sh.edit();
                    ed.putString("ipaddress", ip);
                    ed.putString("url", url);
                    ed.commit();
                    Intent i = new Intent(getApplicationContext(), login.class);
                    startActivity(i);
                }
            }
        });
    }
}