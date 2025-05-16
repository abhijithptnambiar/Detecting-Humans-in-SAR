package com.example.detecting_humans_in_sar;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class login extends AppCompatActivity {
    EditText name,password;
    Button login;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        name=findViewById(R.id.editTextTextPersonName);
        password=findViewById(R.id.editTextTextPersonName2);
        login=findViewById(R.id.button);


        SharedPreferences sh=PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        String url=sh.getString("url","")+"/login_res";

        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String un = name.getText().toString();
                String pass = password.getText().toString();
                int flag = 0;
                if (un.equalsIgnoreCase("")) {
                    name.setError("Required");
                    flag++;
                }
                if (pass.equalsIgnoreCase("")) {
                    password.setError("Required");
                    flag++;
                }
                if (flag == 0) {
                    RequestQueue requestQueue = Volley.newRequestQueue(getApplicationContext());
                    StringRequest postRequest = new StringRequest(Request.Method.POST, url,
                            new Response.Listener<String>() {
                                @Override
                                public void onResponse(String response) {
                                    //  Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();

                                    // response
                                    try {
                                        JSONObject jsonObj = new JSONObject(response);
                                        if (jsonObj.getString("status").equalsIgnoreCase("ok")) {

                                            String lid = jsonObj.getString("lid");
                                            String type = jsonObj.getString("type");
                                            SharedPreferences sh = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
                                            SharedPreferences.Editor ed = sh.edit();
                                            ed.putString("lid", lid);
                                            ed.commit();
//                                      if(type.equalsIgnoreCase("rescue"))
//                                      {
                                            Toast.makeText(login.this, "Login success", Toast.LENGTH_SHORT).show();
                                            Intent i = new Intent(getApplicationContext(), home.class);
                                            startActivity(i);
                                            Intent k = new Intent(getApplicationContext(), home.class);
                                            startService(k);
//                                      }

                                            // ArrayAdapter<String> adpt=new ArrayAdapter<String>(getApplicationContext(),android.R.layout.simple_list_item_1,name);
                                            // l1.setAdapter(new Custom(getApplicationContext(),gamecode,name,type,discription,image,status));
                                        }


                                        // }
                                        else {
                                            Toast.makeText(getApplicationContext(), "Invalid Authentication", Toast.LENGTH_LONG).show();
                                        }

                                    } catch (Exception e) {
                                        Toast.makeText(getApplicationContext(), "Error" + e.getMessage().toString(), Toast.LENGTH_SHORT).show();
                                    }
                                }
                            },
                            new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                    // error
                                    Toast.makeText(getApplicationContext(), "eeeee" + error.toString(), Toast.LENGTH_SHORT).show();
                                }
                            }
                    ) {
                        @Override
                        protected Map<String, String> getParams() {
                            SharedPreferences sh = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
                            Map<String, String> params = new HashMap<String, String>();


                            params.put("username", un);
                            params.put("password", pass);


                            return params;
                        }
                    };

                    int MY_SOCKET_TIMEOUT_MS = 100000;

                    postRequest.setRetryPolicy(new DefaultRetryPolicy(
                            MY_SOCKET_TIMEOUT_MS,
                            DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                            DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
                    requestQueue.add(postRequest);
                }
            }
        });






    }
}