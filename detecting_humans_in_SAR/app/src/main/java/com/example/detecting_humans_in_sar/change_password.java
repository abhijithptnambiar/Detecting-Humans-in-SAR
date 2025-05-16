package com.example.detecting_humans_in_sar;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
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

public class change_password extends AppCompatActivity {
    EditText oldpas,newpas,confirmpas;
    Button change;
    String password_pattern="(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_change_password);
        oldpas=findViewById(R.id.editTextTextPersonName3);
        newpas=findViewById(R.id.editTextTextPersonName4);
        confirmpas=findViewById(R.id.editTextTextPersonName5);
        change=findViewById(R.id.button2);


        SharedPreferences sh=PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        String url=sh.getString("url","")+"/change_password";
        change.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //String un=name.getText().toString();
                String op = oldpas.getText().toString();
                String np = newpas.getText().toString();
                String cp = confirmpas.getText().toString();
                int flag=0;
                if(op.equalsIgnoreCase("")){
                    oldpas.setError("Required");
                    flag++;
//                    Toast.makeText(MainActivity.this, "", Toast.LENGTH_SHORT).show();
                }
                if(!np.matches(password_pattern)){
                    newpas.setError("Password pattern missmatches");
                    flag++;
//                    Toast.makeText(MainActivity.this, "", Toast.LENGTH_SHORT).show();
                }
                if(!cp.matches(np)){
                    confirmpas.setError("Not same as new password");
                    flag++;
//                    Toast.makeText(MainActivity.this, "", Toast.LENGTH_SHORT).show();
                }
                if(flag==0) {
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

                                        Toast.makeText(change_password.this, "Password changed successfully", Toast.LENGTH_SHORT).show();
                                        Intent i=new Intent(getApplicationContext(),home.class);
                                        startActivity(i);
//

                                        // ArrayAdapter<String> adpt=new ArrayAdapter<String>(getApplicationContext(),android.R.layout.simple_list_item_1,name);
                                        // l1.setAdapter(new Custom(getApplicationContext(),gamecode,name,type,discription,image,status));
                                    }
                                    else if (jsonObj.getString("status").equalsIgnoreCase("no")) {

                                        Toast.makeText(change_password.this, "Oops try again :(", Toast.LENGTH_SHORT).show();
                                        Intent i=new Intent(getApplicationContext(),change_password.class);
                                        startActivity(i);
//

                                        // ArrayAdapter<String> adpt=new ArrayAdapter<String>(getApplicationContext(),android.R.layout.simple_list_item_1,name);
                                        // l1.setAdapter(new Custom(getApplicationContext(),gamecode,name,type,discription,image,status));
                                    }


                                    // }
                                    else {
                                        Toast.makeText(getApplicationContext(), "Not found", Toast.LENGTH_LONG).show();
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

//                        String id = sh.getString("lid", "");
                        params.put("lid", sh.getString("lid",""));
                        //params.put("username",un);
                        params.put("oldpassword", op);
                        params.put("newpassword", np);
                        params.put("confirmpassword", cp);
//                params.put("mac",maclis);

                        return params;
                    }
                };

                int MY_SOCKET_TIMEOUT_MS = 100000;

                postRequest.setRetryPolicy(new DefaultRetryPolicy(
                        MY_SOCKET_TIMEOUT_MS,
                        DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                        DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
                requestQueue.add(postRequest);
            }}
        });
    }
}
