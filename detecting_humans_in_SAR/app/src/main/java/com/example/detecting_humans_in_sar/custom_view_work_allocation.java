package com.example.detecting_humans_in_sar;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;


public class custom_view_work_allocation extends BaseAdapter {

    String[] wid,date,details, work, address, longitude, latitude,status;
    private Context context;

    public custom_view_work_allocation(Context appcontext,String[] wid,String[] date,String[] details, String[] work, String[] address, String[] longitude, String[] latitude,String[] status)
    {
        this.context=appcontext;
        this.wid=wid;
        this.date=date;
        this.details=details;
        this.work=work;
        this.address=address;
        this.longitude=longitude;
        this.latitude=latitude;
        this.status=status;



    }

    @Override
    public int getCount() {
        return date.length;
    }

    @Override
    public Object getItem(int i) {
        return null;
    }

    @Override
    public long getItemId(int i) {
        return 0;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        LayoutInflater inflator=(LayoutInflater)context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);

        View gridView;
        if(view==null)
        {
            gridView=new View(context);
            //gridView=inflator.inflate(R.layout.customview, null);
            gridView=inflator.inflate(R.layout.activity_custom_view_work_allocation,null);

        }
        else
        {
            gridView=(View)view;

        }

        Button b_update=(Button)gridView.findViewById(R.id.button6);
        Button b_locate=(Button)gridView.findViewById(R.id.button5);
        b_locate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String url = "https://www.google.com/maps/?q="+latitude[i]+","+longitude[i];
                Intent i = new Intent(android.content.Intent.ACTION_VIEW,Uri.parse(url));
                i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                context.startActivity(i);
            }
        });

        b_update.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                SharedPreferences sh=PreferenceManager.getDefaultSharedPreferences(context.getApplicationContext());
                SharedPreferences.Editor ed=sh.edit();
                ed.putString("wid",wid[i]);
                ed.commit();
                Intent i=new Intent(context.getApplicationContext(),send_amount.class);
                i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                context.startActivity(i);
            }
        });
//        if (!status[i].equalsIgnoreCase("paid")) {
//            b_update.setVisibility(View.VISIBLE);
//        } else {
//            b_update.setVisibility(View.GONE);
//        }
        if (!status[i].equalsIgnoreCase("paid")) {
            b_update.setEnabled(true);  // Button is enabled if status is not "paid"
        } else {
            b_update.setEnabled(false); // Button is disabled if status is "paid"
        }


//        b_update.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                SharedPreferences sh = PreferenceManager.getDefaultSharedPreferences(context);
//                String url = sh.getString("url","")+"/update_status";
//
//                RequestQueue requestQueue = Volley.newRequestQueue(context);
//                StringRequest postRequest = new StringRequest(Request.Method.POST, url,
//                        new Response.Listener<String>() {
//                            @Override
//                            public void onResponse(String response) {
//                                //  Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();
//
//                                // response
//                                try {
//                                    JSONObject jsonObj = new JSONObject(response);
//                                    if (jsonObj.getString("status").equalsIgnoreCase("ok")) {
//
//                                        Toast.makeText(context, "Status updated", Toast.LENGTH_SHORT).show();
//                                        Intent i=new Intent(context,home.class);
//                                        i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
//                                        context.startActivity(i);
//                                    }
//
//
//                                    // }
//                                    else {
//                                        Toast.makeText(context, "Not found", Toast.LENGTH_LONG).show();
//                                    }
//
//                                }    catch (Exception e) {
//                                    Toast.makeText(context, "Error" + e.getMessage().toString(), Toast.LENGTH_SHORT).show();
//                                }
//                            }
//                        },
//                        new Response.ErrorListener() {
//                            @Override
//                            public void onErrorResponse(VolleyError error) {
//                                // error
//                                Toast.makeText(context, "eeeee" + error.toString(), Toast.LENGTH_SHORT).show();
//                            }
//                        }
//                ) {
//                    @Override
//                    protected Map<String, String> getParams() {
//                        SharedPreferences sh = PreferenceManager.getDefaultSharedPreferences(context);
//                        Map<String, String> params = new HashMap<String, String>();
//
//
//
//                        params.put("wid",wid[i]);
//
//                        return params;
//                    }
//                };
//
//                int MY_SOCKET_TIMEOUT_MS=100000;
//
//                postRequest.setRetryPolicy(new DefaultRetryPolicy(
//                        MY_SOCKET_TIMEOUT_MS,
//                        DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
//                        DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
//                requestQueue.add(postRequest);
//            }
//        });




        TextView tv_date=(TextView)gridView.findViewById(R.id.textView2);
        tv_date.setTextColor(Color.BLACK);
        tv_date.setText(date[i]);

        TextView tv_work=(TextView)gridView.findViewById(R.id.textView4);
        tv_work.setTextColor(Color.BLACK);
        tv_work.setText(work[i]);

        TextView tv_details=(TextView)gridView.findViewById(R.id.textView6);
        tv_details.setTextColor(Color.BLACK);
        tv_details.setText(details[i]);

        TextView tv_address=(TextView)gridView.findViewById(R.id.textView8);
        tv_address.setTextColor(Color.BLACK);
        tv_address.setText(address[i]);


//        TextView tv_longitude=(TextView)gridView.findViewById(R.id.textView10);
//        tv_longitude.setTextColor(Color.BLACK);
//        tv_longitude.setText(longitude[i]);

//        TextView tv_latitude=(TextView)gridView.findViewById(R.id.textView10);
//        tv_latitude.setTextColor(Color.BLACK);
//        tv_latitude.setText(latitude[i]);

        return gridView;
    }
}
